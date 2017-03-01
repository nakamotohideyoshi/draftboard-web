from collections import Counter

from django.db.models import F
from django.db.transaction import atomic

import ticket.models
from cash.classes import CashTransaction
from contest.serializers import (
    ContestPoolSerializer,
)
from dfslog.classes import Logger, ErrorCodes
from lineup.classes import (
    LineupManager,
)
from lineup.exceptions import (
    LineupDoesNotMatchUser,
    LineupDoesNotMatchExistingEntryLineup,
)
from lineup.models import (
    Lineup,
)
from mysite.classes import AbstractSiteUserClass
from push.classes import (
    ContestPoolPush,
)
from ticket.classes import TicketManager
from ticket.exceptions import UserDoesNotHaveTicketException
from .models import Buyin
from ..exceptions import (
    ContestLineupMismatchedDraftGroupsException,
    ContestIsInProgressOrClosedException,
    ContestIsFullException,
    ContestMaxEntriesReachedException,
    ContestIsNotAcceptingLineupsException,
)
from ..models import (
    # Contest,
    Entry,
    ContestPool,
)


class BuyinManager(AbstractSiteUserClass):
    """
    Responsible for performing the buyins for all active contests for both
    cash and ticket games.
    """

    def __init__(self, user):
        super().__init__(user)

    def validate_arguments(self, contest_pool, lineup=None):
        """
        Verifies that contest and lineup are instances
        of :class:`contest.models.ContestPool` and :class:`lineup.models.Lineup`
        :param contest_pool:
        :param lineup:
        :return:
        """
        #
        # validation if the contest argument
        self.validate_variable(ContestPool, contest_pool)

        #
        # validation if the lineup argument
        self.validate_variable(Lineup, lineup)

    @atomic
    def buyin(self, contest_pool, lineup=None):
        """
        Creates the buyin for the user based on the ContestPool and lineup. Lineup can
        be null or not passed to allow for reserving contest spots.

        This should be only run in a task

        :param contest_pool: the ContestPool to register in
        :param lineup: assumed the lineup is validated on creation

        :raises :class:`contest.exceptions.ContestCouldNotEnterException`: When the
        there is a race condition and the contest cannot be entered after max_retries
        :raises :class:`contest.exceptions.ContestIsNotAcceptingLineupsException`: When
            contest_pool does not have a draftgroup, because it is not accepting teams yet.
        :raises :class:`contest.exceptions.ContestLineupMismatchedDraftGroupsException`:
            When the lineup was picked from a draftgroup that does not match the contest_pool.
        :raises :class:`contest.exceptions.ContestIsInProgressOrClosedException`: When
            The contest_pool has started, or its past the start time
        :raises :class:`contest.exceptions.LineupDoesNotMatchUser`: When the lineup
            is not owned by the user.
        :raises :class:`contest.exceptions.ContestMaxEntriesReachedException`: When the
            max entries is reached by the lineup.
        """

        # validate the contest and the lineup are allowed to be created
        self.lineup_contest(contest_pool, lineup)

        # Create either the ticket or cash transaction
        # Try to pay with a ticket first, if that doesn't work because the user doesn't have any
        # tickets, then try to pay with their cash balance.
        tm = TicketManager(self.user)
        # Get the transaction type - `ContestBuyin`
        # category = TransactionType.objects.get(pk=TransactionTypeConstants.ContestBuyin)

        try:
            tm.consume(amount=contest_pool.prize_structure.buyin)
            # keep a reference of the transaction.
            transaction = tm.transaction

        except (UserDoesNotHaveTicketException, ticket.models.TicketAmount.DoesNotExist):
            # Paying via Ticket failed, Create a cash transaciton with the type of 'ContestBuyin'.
            ct = CashTransaction(user=self.user)
            # Make the transaction a withdrawal.
            ct.withdraw(amount=contest_pool.prize_structure.buyin)
            # keep a reference of the transaction for user later.
            transaction = ct.transaction

        #
        # Transfer money into escrow
        escrow_ct = CashTransaction(self.get_escrow_user())
        escrow_ct.deposit(contest_pool.prize_structure.buyin, trans=transaction)

        #
        # Create the Entry
        entry = Entry()
        entry.contest_pool = contest_pool
        # entry.contest = contest # the contest will be set later when the ContestPool starts
        entry.contest = None
        entry.lineup = lineup
        entry.user = self.user
        entry.save()

        #
        # Create the Buyin model
        buyin = Buyin()
        buyin.transaction = transaction
        # buyin.contest = contest # the contest will be set later when the ContestPool starts (?)
        buyin.contest = None
        buyin.entry = entry
        buyin.save()

        #
        # Increment the contest_entry variable
        contest_pool.current_entries = F('current_entries') + 1
        contest_pool.save()
        contest_pool.refresh_from_db()

        msg = "User[" + self.user.username + "] bought into the contest_pool #" \
              + str(contest_pool.pk) + " with entry #" + str(entry.pk)
        Logger.log(ErrorCodes.INFO, "ContestPool Buyin", msg)

        #
        # pusher contest updates because entries were changed
        ContestPoolPush(ContestPoolSerializer(contest_pool).data).send()

    def lineup_contest(self, contest_pool, lineup=None):
        """
        Verifies the lineup and contest_pool can be submitted
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
        self.validate_arguments(contest_pool, lineup)

        #
        # Make sure the contest has a draftgroup if there is a lineup
        if lineup is not None and contest_pool.draft_group is None:
            raise ContestIsNotAcceptingLineupsException()

        #
        # Make sure they share draftgroups
        if lineup is not None and contest_pool.draft_group.pk != lineup.draft_group.pk:
            raise ContestLineupMismatchedDraftGroupsException()

        #
        # Make sure the contest status is not past the time when you could buyin
        if contest_pool.is_started():
            raise ContestIsInProgressOrClosedException()

        self.check_contest_full(contest_pool)

        #
        # Verify the lineup is the User's Lineup
        if lineup is not None and lineup.user != self.user:
            raise LineupDoesNotMatchUser()

        # get the current entry objects for the user
        entries = self.get_user_entries(contest_pool)

        # Make sure that a contest cannot be entered and the user has not entered
        # more teams than they are allowed.
        if len(entries) >= contest_pool.max_entries:
            raise ContestMaxEntriesReachedException()

            # ensure the lineup attempting to be submitted
            # is the same as any existing lineups.
            # raises LineupDoesNotMatchExisting

            # This is disabled because we are now allowing multiple lineups from one user to be entered
            # into the same contest.
            # self.validate_lineup_players_match_existing_entries(lineup, entries)

    def validate_lineup_players_match_existing_entries(self, lineup, entries):
        """
        validate the lineup has the same players as any entries that already exist

        :param lineup: the lineup attempted to be entered
        :param entries: entry objects which 'lineup' must be equivalent to (ie: have the same players)
        :return:
        """
        # print('+---------------------------------------------+')
        # print('lineup name:', str(lineup.name))
        if len(entries) == 0:
            return

        lm = LineupManager(self.user)
        player_srids = lm.get_player_srids(lineup)

        for entry in entries:
            if entry.lineup is None:
                continue
            entry_lineup_player_srids = lm.get_player_srids(entry.lineup)
            if Counter(player_srids) != Counter(entry_lineup_player_srids):
                # debug
                # print('Counter(player_srids) != Counter(entry_lineup_player_srids)')
                # print('lineup       :', str(dict(Counter(player_srids))))
                # print('entry lineup :', str(dict(Counter(entry_lineup_player_srids))))
                err_msg = "Lineup must match the existing lineup '%s' for this Contest." % lineup.name
                raise LineupDoesNotMatchExistingEntryLineup(err_msg)

                # print('+---------------------------------------------+')

    def get_user_entries(self, contest_pool):
        """
        get a queryset of the user's entries currently in the ContestPool
        :param contest_pool:
        :return:
        """
        return Entry.objects.filter(user=self.user, contest_pool=contest_pool)

    @staticmethod
    def check_contest_full(contest_pool):
        """
        Method takes in a contest and throws an
        :class:`contest.exceptions.ContestIsFullException` exception
        if the contest is full
        :param contest:

        :raises :class:`contest.exceptions.ContestIsFullException`: When the contest is full
            and is no longer accepting new entries.
        """

        #
        # 'entries' field defaults to 0, which indicates there is not cap,
        # however if it is non-zero, then it is a capped contest_pool (capped total contest pool entries)
        if contest_pool.entries != 0 and contest_pool.current_entries >= contest_pool.entries:
            raise ContestIsFullException()

    def entry_did_use_ticket(self, entry):
        self.validate_variable(Entry, entry)
        buyin = Buyin.objects.get(entry=entry)
        try:
            ticket.models.Ticket.objects.get(consume_transaction=buyin.transaction)
            return True
        except ticket.models.Ticket.DoesNotExist:
            return False
