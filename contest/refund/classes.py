from mysite.classes import AbstractSiteUserClass
from ..models import Entry, Contest
from contest.buyin.classes import BuyinManager
from ticket.classes import TicketManager
from cash.classes import CashTransaction
from .models import Refund
from django.db.transaction import atomic
from ..exceptions import ContestIsInProgressOrClosedException

class RefundManager(AbstractSiteUserClass):
    """
    Responsible for performing the refunds for all active contests for both
    cash and ticket games.
    """

    def __init__(self, user):
        super().__init__(user)

    def validate_arguments(self, contest):
        """
        Verifies that contest is an instances
        of :class:`contest.models.Contest`
        :param contest:

        """
        #
        # validation if the contest argument
        self.validate_variable(Contest, contest)


    @atomic
    def refund(self, contest):
        #TODO make a task and test in the test script with celery running
        #TODO special ID to prevent other refunds from runnint at same time
        """
        Task that refunds all contest entries and sets the contest to Cancelled
        :param contest:

        :raises :class:`contest.exceptions.ContestIsInProgressOrClosedException`: When
            The contest has either started, been cancelled, or is completed. This
            will keep the site from mistakenly cancelling contests that should not
            be cancelled.
        """
        self.validate_arguments(contest)

        # verify the contest is the correct status
        if contest.status not in Contest.STATUS_UPCOMING:
            raise ContestIsInProgressOrClosedException()


        #
        # get all entries for a contest
        entries = Entry.objects.filter(contest=contest)

        #
        # For all entries create a refund transaction and deposit the
        # cash or ticket back into the user's account
        buyin = contest.prize_structure.buyin
        for entry in entries:
            bm = BuyinManager(entry.user)

            #
            # Create refund transaction from escrow
            escrow_ct = CashTransaction(self.get_escrow_user())
            escrow_ct.withdraw(buyin)
            transaction = escrow_ct.transaction

            #
            # Create a cash or ticket deposit based on what the user
            # used to get into the contest
            if bm.entry_did_use_ticket(entry):
                tm = TicketManager(entry.user)
                tm.deposit(buyin, transaction_obj=transaction)
                self.__create_refund(transaction, entry)
            else:
                ct = CashTransaction(entry.user)
                ct.deposit(buyin, trans=transaction)
                self.__create_refund(transaction, entry)

        #
        # set the contest to cancelled
        contest.status = Contest.CANCELLED
        contest.save()


    def __create_refund(self, transaction, entry):
        """
        Creates the :class:`contest.refund.models.Refund` object based on
        the transaction and entry that was refunded.
        :param transaction:
        :param entry:
        """
        refund = Refund()
        refund.contest = entry.contest
        refund.entry = entry
        refund.transaction = transaction
        refund.save()
