from django.conf import settings
from mysite.classes import AbstractSiteUserClass
from contest.models import Contest
import mysite.exceptions
from lineup.models import Lineup
from ..exceptions import ContestLineupMismatchedDraftGroupsException, ContestIsInProgressOrClosedException, ContestIsFullException, ContestCouldNotEnterException
from django.db.transaction import atomic
from django.db import IntegrityError
from cash.classes import CashTransaction
from ..models import Entry, Contest
from .models import Buyin
from lineup.exceptions import LineupDoesNotMatchUser
from dfslog.classes import Logger, ErrorCodes
class BuyinManager(AbstractSiteUserClass):
    """
    Responsible for performing the buyins for all active contests for both
    cash and ticket games.
    """

    def __init__(self, user):
        super(user)

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

        """
        #
        # validate the contest and the lineup are allowed to be created
        self.lineup_contest(contest,lineup)

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
            #
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
        Creates the entry, buyin, and cash transaction in one atomic method.
        :param contest:
        :param lineup: assumed the lineup is validated on creation
        """
        #
        # Create either the ticket or cash transaction
        ct = CashTransaction(self.user)
        ct.withdraw(contest.prize_structure.buyin)

        #
        # Create the Entry
        entry = Entry()
        entry.contest = contest
        entry.lineup = lineup
        entry.save()

        #
        # Create the Buyin model
        buyin = Buyin()
        buyin.transaction = ct.transaction
        buyin.contest = contest
        buyin.entry = entry
        buyin.save()

        #
        # Increment the contest_entry variable
        contest.current_entries +=1
        contest.save()

        return entry

    def lineup_contest(self, contest, lineup=None):
        """
        Verifies the lineup and contest can be submitted
        together.
        :param contest:
        :param lineup:
        :return:
        """
        self.validate_arguments(contest,lineup)

        #
        # Make sure they share draftgroups
        if lineup is not None and contest.draft_group.pk != lineup.draftgroup.pk :
            raise ContestLineupMismatchedDraftGroupsException()

        #
        # Make sure the contest is accepting new entries
        if contest.current_entries >= contest.entries:
            raise ContestIsFullException()
        #
        # Make sure the contest status is active
        if contest.status not in Contest.STATUS_UPCOMING:
            raise ContestIsInProgressOrClosedException()

        #
        # Verify the lineup is the User's Lineup
        if lineup is not None and lineup.user != self.user:
            raise LineupDoesNotMatchUser()

