from mysite.classes import AbstractSiteUserClass
from lineup.models import Lineup
from ..exceptions import ContestLineupMismatchedDraftGroupsException, ContestIsInProgressOrClosedException, ContestIsFullException, ContestCouldNotEnterException, ContestMaxEntriesReachedException, ContestIsNotAcceptingLineupsException
from django.db.transaction import atomic
from django.db import IntegrityError
from cash.classes import CashTransaction
from ticket.classes import TicketManager
from ..models import Entry, Contest
from .models import Buyin
from lineup.exceptions import LineupDoesNotMatchUser
from dfslog.classes import Logger, ErrorCodes
from ticket.exceptions import  UserDoesNotHaveTicketException
import ticket.models
import traceback
import sys
from django.db.models import F

class BuyinManager(AbstractSiteUserClass):
    """
    Responsible for performing the buyins for all active contests for both
    cash and ticket games.
    """

    def __init__(self, user):
        super().__init__(user)

    def validate_arguments(self, contest, lineup=None):
        """
        Verifies that contest and lineup are instances
        of :class:`contest.models.Contest` and :class:`lineup.models.Lineup`
        :param contest:
        :param lineup:
        :return:
        """
        #
        # validation if the contest argument
        self.validate_variable(Contest, contest)

        #
        # validation if the lineup argument
        self.validate_variable(Lineup, lineup)

    def buyin(self, contest, lineup=None):
        """
        Creates the buyin for the user based on the contest and lineup. Lineup can
        be null or not passed to allow for reserving contest spots.
        :param contest:
        :param lineup: assumed the lineup is validated on creation

        :raises :class:`contest.exceptions.ContestCouldNotEnterException`: When the
        there is a race condition and the contest cannot be entered after max_retries
        :raises :class:`contest.exceptions.ContestIsNotAcceptingLineupsException`: When
            contest does not have a draftgroup, because it is not accepting teams yet. The
            contest will most likely be a future contest.
        :raises :class:`contest.exceptions.ContestLineupMismatchedDraftGroupsException`:
            When the lineup was picked from a draftgroup that does not match the contest.
        :raises :class:`contest.exceptions.ContestIsInProgressOrClosedException`: When
            The contest has either started, been cancelled, or is completed.
        :raises :class:`contest.exceptions.LineupDoesNotMatchUser`: When the lineup
            is not owned by the user.
        :raises :class:`contest.exceptions.ContestMaxEntriesReachedException`: When the
            max entries is reached by the lineup.
        :raises :class:`contest.exceptions.ContestIsFullException`: When the contest is full
            and is no longer accepting new entries.
        """
        #
        # validate the contest and the lineup are allowed to be created
        self.lineup_contest(contest, lineup)

        max_retries = 5
        i = 0
        #
        # Retries if there is a concurrency error
        while i < max_retries:
            try:
                entry = self.__create_buyin_entry(contest, lineup)
                #
                # Contest entry successful
                msg = "User["+self.user.username+"] bought into the contest #"\
                      +str(contest.pk)+" with entry #"+str(entry.pk)
                Logger.log(ErrorCodes.INFO, "Contest Buyin", msg )
                return

            # throws integrity error if there is a race condition on the
            # contest.current_entries field
            except IntegrityError:
                if contest.current_entries >= contest.entries:
                    #
                    # Contest is full
                    msg = "User["+self.user.username+"] tried to buyin into the" \
                            " contest #"+str(contest.pk)+" but the contest was full"
                    Logger.log(ErrorCodes.INFO, "Contest Full", msg )
                    raise ContestIsFullException()
            i+=1

        #
        # Worst case scenario when there have been max_retries attempts to
        # create an buyin entry.
        msg = "User["+self.user.username+"] could not enter contest #"+str(contest.pk)+\
              " after "+str(max_retries)+" retries due to race conditions"
        Logger.log(ErrorCodes.ERROR, "Contest Buyin", msg )
        raise ContestCouldNotEnterException()

    @atomic
    def __create_buyin_entry(self, contest, lineup=None):
        """
        Creates the entry, buyin, and cash transaction from user to escrow
        in one atomic method.
        :param contest:
        :param lineup: assumed the lineup is validated on creation

        :raises :class:`contest.exceptions.ContestIsNotAcceptingLineupsException`: When
            contest does not have a draftgroup, because it is not accepting teams yet. The
            contest will most likely be a future contest.
        :raises :class:`contest.exceptions.ContestLineupMismatchedDraftGroupsException`:
            When the lineup was picked from a draftgroup that does not match the contest.
        :raises :class:`contest.exceptions.ContestIsInProgressOrClosedException`: When
            The contest has either started, been cancelled, or is completed.
        :raises :class:`contest.exceptions.LineupDoesNotMatchUser`: When the lineup
            is not owned by the user.
        :raises :class:`contest.exceptions.ContestMaxEntriesReachedException`: When the
            max entries is reached by the lineup.
        :raises :class:`contest.exceptions.ContestIsFullException`: When the contest is full
            and is no longer accepting new entries.
        """
        #
        # Create either the ticket or cash transaction
        tm = TicketManager(self.user)
        try:
            tm.consume(amount=contest.prize_structure.buyin)
            transaction = tm.transaction

        except (UserDoesNotHaveTicketException, ticket.models.TicketAmount.DoesNotExist):
            ct = CashTransaction(self.user)
            ct.withdraw(contest.prize_structure.buyin)
            transaction = ct.transaction
        #
        # Transfer money into escrow
        escrow_ct = CashTransaction(self.get_escrow_user())
        escrow_ct.deposit(contest.prize_structure.buyin, trans=transaction)

        #
        # Create the Entry
        entry = Entry()
        entry.contest = contest
        entry.lineup = lineup
        entry.user = self.user
        entry.save()

        #
        # Create the Buyin model
        buyin = Buyin()
        buyin.transaction = transaction
        buyin.contest = contest
        buyin.entry = entry
        buyin.save()

        #
        # Increment the contest_entry variable
        self.check_contest_full(contest)
        contest.current_entries = F('current_entries') + 1
        contest.save()
        contest.refresh_from_db()

        return entry


    def lineup_contest(self, contest, lineup=None):
        """
        Verifies the lineup and contest can be submitted
        together.
        :param contest:
        :param lineup:

        :raises :class:`contest.exceptions.ContestIsNotAcceptingLineupsException`: When
            contest does not have a draftgroup, because it is not accepting teams yet. The
            contest will most likely be a future contest.
        :raises :class:`contest.exceptions.ContestLineupMismatchedDraftGroupsException`:
            When the lineup was picked from a draftgroup that does not match the contest.
        :raises :class:`contest.exceptions.ContestIsInProgressOrClosedException`: When
            The contest has either started, been cancelled, or is completed.
        :raises :class:`contest.exceptions.LineupDoesNotMatchUser`: When the lineup
            is not owned by the user.
        :raises :class:`contest.exceptions.ContestMaxEntriesReachedException`: When the
            max entries is reached by the lineup.
        :raises :class:`contest.exceptions.ContestIsFullException`: When the contest is full
            and is no longer accepting new entries.

        """
        self.validate_arguments(contest,lineup)

        #
        # Make sure the contest has a draftgroup if there is a lineup
        if lineup is not None and contest.draft_group is None:
            raise ContestIsNotAcceptingLineupsException()

        #
        # Make sure they share draftgroups
        if lineup is not None and contest.draft_group.pk != lineup.draftgroup.pk:
            raise ContestLineupMismatchedDraftGroupsException()

        self.check_contest_full(contest)
        #
        # Make sure the contest status is active
        if contest.status not in Contest.STATUS_UPCOMING:
            raise ContestIsInProgressOrClosedException()

        #
        # Verify the lineup is the User's Lineup
        if lineup is not None and lineup.user != self.user:
            raise LineupDoesNotMatchUser()

        #
        # Make sure that a contest cannot be entered and the user has not entered
        # more teams than they are allowed.
        entries = Entry.objects.filter(user=self.user, contest=contest)
        if len(entries) >= contest.max_entries:
            raise ContestMaxEntriesReachedException()

    def check_contest_full(self, contest):
        """
        Method takes in a contest and throws an
        :class:`contest.exceptions.ContestIsFullException` exception
        if the contest is full
        :param contest:

        :raises :class:`contest.exceptions.ContestIsFullException`: When the contest is full
            and is no longer accepting new entries.
        """
        if contest.current_entries >= contest.entries:
            raise ContestIsFullException()

    def entry_did_use_ticket(self,entry):
        self.validate_variable(Entry, entry)
        buyin = Buyin.objects.get(entry=entry)
        buyin.transaction
        try:
            ticket.models.Ticket.objects.get(transaction=buyin.transaction)
            return True
        except ticket.models.Ticket.DoesNotExist:
            return False
