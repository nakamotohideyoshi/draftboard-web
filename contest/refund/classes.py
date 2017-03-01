from logging import getLogger

from django.db.models import F
from django.db.transaction import atomic

from cash.classes import CashTransaction
from contest.buyin.classes import BuyinManager
from contest.serializers import (
    ContestPoolSerializer,
)
from dfslog.classes import Logger, ErrorCodes
from mysite.classes import AbstractManagerClass
from push.classes import (
    ContestPoolPush,
)
from ticket.classes import TicketManager
from .exceptions import (
    EntryCanNotBeUnregisteredException,
    UnmatchedEntryIsInContest
)
from .models import Refund
from ..exceptions import ContestCanNotBeRefunded
from ..models import (
    Entry,
    Contest,
    LiveContest,
    HistoryContest,
)

logger = getLogger('contest.refund.classes')


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

    @staticmethod
    def __validate_entry_can_be_unregistered(entry):
        """
        :param entry:
        :raises EntryCanNotBeUnregisteredException: raised if the Contest is full, or inprogress/closed
        """

        if entry.contest is not None:
            # if the contest is non-null, then the ContestPool has created
            # the contest and set it -- this means its in progress
            raise EntryCanNotBeUnregisteredException(
                'The contest is running and you may no longer unregister.')

    @atomic
    def remove_and_refund_entry(self, entry):
        """
        refunds the buyin for the entry, and completely removes it from the ContestPool.

        This runs when a user deregisters from a contest.

        :param entry:
        :return:
        """

        # ensures the Entry can be unregistered from the ContestPool its associated with.
        self.__validate_entry_can_be_unregistered(entry)

        # refund the buyin
        refund = self.__refund_entry(entry)

        # remove the entry from the contest, and cleanup contest properties
        contest_pool = entry.contest_pool
        contest_pool.current_entries = F('current_entries') - 1  # true atomic decrement
        contest_pool.save()
        contest_pool.refresh_from_db()

        msg = "User[" + entry.user.username + "] unregistered from the contest_pool #" \
              + str(contest_pool.pk) + " with entry #" + str(entry.pk)
        Logger.log(ErrorCodes.INFO, "ContestPool Unregister", msg)

        # pusher contest updates because entries were changed
        ContestPoolPush(ContestPoolSerializer(contest_pool).data).send()

        # entirely delete the entry, since the user's lineup is no longer in the contest
        entry.delete()
        return refund

    @atomic
    def refund_unmatched_entry(self, entry):
        """
        Refund unmatched entry. After a contest pool spawns into contests, any unmatched entries
        need to be refunded. These entries were never in contests, so they obviously will not
        be removed from anything.

        :param entry: The unmatched entry to refund.
        """

        # This entry should be one that was not matched, make sure it is not in a contest.
        if entry.contest is not None:
            raise UnmatchedEntryIsInContest(entry)

        # Refund the entry.
        return self.__refund_entry(entry)

    @atomic
    def __refund_entry(self, entry):
        """
        refund a single entry.

        THIS DOES NOT remove the entry from a contest!

        :param entry:
        :return:
        """

        buyin = entry.contest_pool.prize_structure.buyin
        bm = BuyinManager(entry.user)
        transaction = None

        # Create a cash or ticket deposit as a refund,
        # based on what the user used to get into the contest
        if bm.entry_did_use_ticket(entry):
            tm = TicketManager(entry.user)
            tm.deposit(buyin)
            transaction = tm.transaction
            refund = self.__create_refund(transaction, entry)
        else:
            ct = CashTransaction(entry.user)
            ct.deposit(buyin)
            transaction = ct.transaction
            refund = self.__create_refund(transaction, entry)

        # Create refund transaction from escrow
        escrow_ct = CashTransaction(self.get_escrow_user())
        escrow_ct.withdraw(buyin, trans=transaction)
        return refund

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
            self.__refund_entry(entry)

        #
        # after all set the contest to cancelled
        contest.status = Contest.CANCELLED
        contest.save()

    @staticmethod
    def __create_refund(transaction, entry):
        """
        Creates the :class:`contest.refund.models.Refund` object based on
        the transaction and entry that was refunded.
        :param transaction:
        :param entry:
        """
        try:
            r = Refund.objects.get(entry=entry)
            logger.warning('Refund already exists, not issuing another: %s' % r)
        except Refund.DoesNotExist:
            # only create a refund if one doesnt exist
            refund = Refund(
                contest_pool=entry.contest_pool,
                entry=entry,
                transaction=transaction
            )
            refund.save()
            logger.info('Refund created: %s' % refund)
            return refund
