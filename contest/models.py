#
# contest/models.py

from django.db import models
from sports.classes import SiteSportManager

class Contest(models.Model):
    """
    Represents all the settings, and statuses of a Contest.
    """

    #
    # all possible statuses
    RESERVABLE  = 'reservable'
    SCHEDULED   = 'scheduled'
    INPROGRESS  = 'inprogress'
    #COMPLETED   = 'completed'
    CLOSED      = 'closed'
    CANCELLED   = 'cancelled'

    #
    # categories of statuses
    STATUS_UPCOMING = [
        RESERVABLE,
        SCHEDULED
    ]

    STATUS_LIVE = [
        INPROGRESS,
        #COMPLETED
    ]

    STATUS_HISTORY = [
        CLOSED,
        CANCELLED
    ]

    # combination of UPCOMING & LIVE for the main contest lobby
    STATUS_LOBBY_CONTESTS = []
    STATUS_LOBBY_CONTESTS += STATUS_UPCOMING
    STATUS_LOBBY_CONTESTS += STATUS_LIVE

    STATUS_ALL = []
    STATUS_ALL += STATUS_UPCOMING
    STATUS_ALL += STATUS_LIVE
    STATUS_ALL += STATUS_HISTORY

    #
    # group
    STATUS = (
        (
            'Upcoming', (
                (RESERVABLE,    'Reservable'),      # no players pools, but challenge can be bought into
                (SCHEDULED,     'Scheduled'),       # contest is draftable - it hasnt started yet
            )
        ),
        (
            'Live', (
                (INPROGRESS,    'In Progress'),     # game is locked, no new entries
                #(COMPLETED,     'Completed'),       # the live games are completed (but potentially not finalized)
            )
        ),
        (
            'History', (
                (CLOSED,        'Closed'),          # game is paid out, this is a final status
                (CANCELLED,     'Cancelled'),       # game has been refunded, and closed. was not, and wont pay out
            )
        ),

    )

    def __str__(self):
        return 'pk:%-10s | %-16s | %s' % (self.pk, self.status, self.name)

    created = models.DateTimeField(auto_now_add=True)

    site_sport = models.ForeignKey('sports.SiteSport', null=False)

    name = models.CharField(default="",
                            null=False,
                            help_text= "The plain text name of the Contest",
                                                           verbose_name="Name",
                                                           max_length=64)
    prize_structure = models.ForeignKey('prize.PrizeStructure',
                              null=False)
    status = models.CharField(max_length=32,
                              choices=STATUS,
                              default=SCHEDULED,
                              null=False)

    # start & today_only/end determine the range of time,
    # in between which live sporting events will be included
    # and players from them can be drafted
    start       = models.DateTimeField(null=False,
                    verbose_name='The time this contest will start!',
                    help_text='the start should coincide with the start of a real-life game.')
    #today_only  = models.BooleanField(default=True, null=False)
    end         = models.DateTimeField(null=False,
                    verbose_name='the time, after which real-life games will not be included in this contest',
                    help_text='this field is overridden if the TodayOnly box is enabled')

    # set the pool of players this contest can draft from
    draft_group = models.ForeignKey('draftgroup.DraftGroup', null=True,
                    verbose_name='DraftGroup',
                    help_text='the pool of draftable players and their salaries, for the games this contest includes.' )

    def update_status(self):
        """
        Updates the status for the contest based on the player pool's game
        statuses. Once the first game has started for a contest, the status
        should be turned to In Progress. Once the games are completed and
        the stats for the game are set to "closed" in sports radar feeds, the
        game should be set to completed. At this point the payout task
        can be initiated and once all of the places have been paid out, the
        status can be set to closed.
        """
        pass

    def __get_game_model(self):
        ssm = SiteSportManager()
        return ssm.get_game_class(self.site_sport)

    def games(self):
        game_model = self.__get_game_model()
        return game_model.objects.filter( start__gte=self.start, start__lt=self.end )

class LobbyContest(Contest):
    """
    PROXY model for Upcoming & Live Contests ... and rest API use.

    This is the model which gets the Contests for
    display on the home lobby, so make sure you know
    what you are doing if you are making changes.
    """
    class LobbyContestManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status__in=Contest.STATUS_LOBBY_CONTESTS)

    objects = LobbyContestManager()

    class Meta:
        proxy = True

class UpcomingContest(Contest):
    """
    PROXY model for upcoming Contests ... and rest API use.

    This model has access to all contests which have not started yet.
    """

    class UpcomingContestManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status__in=Contest.STATUS_UPCOMING)

    # yes, the UpcomingContest.objects on which you can get() or filter(), etc...
    objects = UpcomingContestManager()

    class Meta:
        proxy = True

class LiveContest(Contest):
    """
    PROXY model for Live Contests ... and rest API use.

    This model can get any Contest which is currently live on the site.
    """

    class LiveContestManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status__in=Contest.STATUS_LIVE)

    objects = LiveContestManager()

    class Meta:
        proxy = True

class HistoryContest(Contest):
    """
    PROXY model for viewing only the Historical contests .. and rest API use.

    This model can get any Contests which are over -- those are any contests
    which have been successfully closed and paid, or were perhaps cancelled or refunded.
    """

    class HistoryContestManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status__in=Contest.STATUS_HISTORY)

    objects = HistoryContestManager()

    class Meta:
        proxy = True

class Entry(models.Model):
    """
    An instance of a Lineup in a Contest. One of these is created
    every time a user pays the entry fee.
    """

    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    contest     = models.ForeignKey(Contest, null=False)
    lineup      = models.ForeignKey("lineup.Lineup")

    def __str__(self):
        return '%s %s' % (self.contest.name, str(self.lineup))

