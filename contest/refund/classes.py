#
# contest/refund/classes.py

from django.db.models import F
from mysite.classes import AbstractManagerClass
from ..models import (
    Entry,
    Contest,
    LiveContest,
    HistoryContest,
)
from contest.buyin.classes import BuyinManager
from ticket.classes import TicketManager
from cash.classes import CashTransaction
from .models import Refund
from django.db.transaction import atomic
from ..exceptions import ContestCanNotBeRefunded
from .exceptions import (
    EntryCanNotBeUnregisteredException,
)

class RefundManager(AbstractManagerClass):
    """
    Responsible for performing the refunds for all active contests for both
    cash and ticket games.
    """

    def __init__(self):
        super().__init__()

    def validate_arguments(self, contest):
        """
        Verifies that contest is an instances
        of :class:`contest.models.Contest`
        :param contest:

        """
        #
        # validation if the contest argument
        self.validate_variable(Contest, contest)

    def __validate_entry_can_be_unregistered(self, entry):
        """
        :param entry:
        :raises EntryCanNotBeUnregisteredException: raised if the Contest is full, or inprogress/closed
        """

        if entry.contest is not None:
            # if the contest is non-null, then the ContestPool has created
            # the contest and set it -- this means its in progress
            raise EntryCanNotBeUnregisteredException('The contest is running and you may no longer unregister.')

    @atomic
    def remove_and_refund_entry(self, entry):
        """
        refunds the buyin for the entry, and completely removes it from the ContestPool.

        :param entry:
        :return:
        """

        # ensures the Entry can be unregistered from the ContestPool its associated with.
        self.__validate_entry_can_be_unregistered(entry)

        # refund the buyin
        self.__refund_entry(entry)

        # remove the entry from the contest, and cleanup contest properties
        contest_pool = entry.contest_pool
        contest_pool.current_entries += F('current_entries') - 1   # true atomic decrement
        contest_pool.save()

        entry.delete()

    @atomic
    def __refund_entry(self, entry):
        """
        refund a single entry.

        THIS DOES NOT remove the entry from a contest!

        :param entry:
        :return:
        """

        buyin           = entry.contest.prize_structure.buyin
        bm              = BuyinManager(entry.user)
        transaction     = None

        #
        # Create a cash or ticket deposit as a refund,
        # based on what the user used to get into the contest
        if bm.entry_did_use_ticket(entry):
            tm = TicketManager(entry.user)
            tm.deposit(buyin)
            transaction = tm.transaction
            self.__create_refund(transaction, entry)
        else:
            ct = CashTransaction(entry.user)
            ct.deposit(buyin)
            transaction = ct.transaction
            self.__create_refund(transaction, entry)

        #
        # Create refund transaction from escrow
        escrow_ct = CashTransaction(self.get_escrow_user())
        escrow_ct.withdraw(buyin, trans=transaction)

    @atomic
    def refund(self, contest, force=False, admin_force=False):
        """
        Task that refunds all contest entries and sets the contest to Cancelled.

        This should only be run in a task on the live site.

        :param contest:

        :raises :class:`contest.exceptions.ContestIsInProgressOrClosedException`: When
            The contest has either started, been cancelled, or is completed. This
            will keep the site from mistakenly cancelling contests that should not
            be cancelled.
        """
        self.validate_arguments(contest)

        if admin_force == False:
            #
            if contest.gpp == True:
                return
            # if its already been cancelled, we cant do it again
            if contest in HistoryContest.objects.all():
                raise ContestCanNotBeRefunded()

        # if we are not forcing the refund, then check if the contest is live first
        if not force:

            if contest not in LiveContest.objects.all():
                raise ContestCanNotBeRefunded()

        #
        # get all entries for a contest
        entries = Entry.objects.filter(contest=contest)

        #
        # For all entries create a refund transaction and deposit the
        # cash or ticket back into the user's account
        for entry in entries:
            self.__refund_entry( entry )

        #
        # after all set the contest to cancelled
        contest.status = Contest.CANCELLED
        contest.save()

    def __create_refund(self, transaction, entry):
        """
        Creates the :class:`contest.refund.models.Refund` object based on
        the transaction and entry that was refunded.
        :param transaction:
        :param entry:
        """
        try:
            r = Refund.objects.get(entry=entry)
        except Refund.DoesNotExist:
            # only create a refund if one doesnt exist
            refund = Refund()
            refund.contest = entry.contest
            refund.entry = entry
            refund.transaction = transaction
            refund.save()
