#
# contest/models.py

from django.db import models
from draftgroup.classes import DraftGroupManager
from sports.classes import SiteSportManager
from django.utils.crypto import get_random_string
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Contest(models.Model):
    """
    Represents all the settings, and statuses of a Contest.
    """

    #
    # all possible statuses
    CLONED      = 'cloned'          # needs admin review and potential modifications
    RESERVABLE  = 'reservable'      # far off contest you can buy into, but cannot draft a team for yet.
    SCHEDULED   = 'scheduled'       # standard draftable contest before it begins
    INPROGRESS  = 'inprogress'      # a live contest!
    COMPLETED   = 'completed'
    CLOSED      = 'closed'          # a paid out contest
    CANCELLED   = 'cancelled'       # a non-guarantee that did not fill up, and did not run (any users were refunded)

    #
    # categories of statuses
    STATUS_UPCOMING = [
        SCHEDULED,   # scheduled first in list because its going to be the default option
        RESERVABLE
    ]

    STATUS_LIVE = [
        INPROGRESS,
        COMPLETED
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
                (COMPLETED,     'Completed'),       # the live games are completed (but potentially not finalized)
            )
        ),
        (
            'History', (
                (CLOSED,        'Closed'),          # game is paid out, this is a final status
                (CANCELLED,     'Cancelled'),       # game has been refunded, and closed. was not, and wont pay out
            )
        ),

    )

    DEFAULT_CID_LENGTH = 6 # the default number of characters in the contest 'cid'

    def __str__(self):
        return 'pk:%-10s | %-16s | %s' % (self.pk, self.status, self.name)

    created = models.DateTimeField(auto_now_add=True)
    cid     = models.CharField(max_length=DEFAULT_CID_LENGTH, default='',
                               null=False, blank=True, editable=False,
                                help_text='unique, randomly chosen when Contest is created')

    site_sport = models.ForeignKey('sports.SiteSport', null=False)

    name = models.CharField(default="", null=False, verbose_name="Public Name", max_length=64,
                            help_text= "The front-end name of the Contest")

    prize_structure = models.ForeignKey('prize.PrizeStructure', null=False)

    status = models.CharField(max_length=32, choices=STATUS, default=STATUS_UPCOMING, null=False)

    # start & today_only/end determine the range of time,
    # in between which live sporting events will be included
    # and players from them can be drafted
    start       = models.DateTimeField(null=False,
                    verbose_name='The time this contest will start!',
                    help_text='the start should coincide with the start of a real-life game.')
    #today_only  = models.BooleanField(default=True, null=False)
    end         = models.DateTimeField(null=False, blank=True,
                    verbose_name='the time, after which real-life games will not be included in this contest',
                    help_text='forces the end time of the contest (will override "Ends tonight" checkbox!!')

    # set the pool of players this contest can draft from
    draft_group = models.ForeignKey('draftgroup.DraftGroup', null=True,
                    verbose_name='DraftGroup',
                    help_text='the pool of draftable players and their salaries, for the games this contest includes.' )


    max_entries = models.PositiveIntegerField(null=False,
                                              default=1,
                                              help_text="The total number of entries a user can add to a contest")

    entries = models.PositiveIntegerField(null=False,
                                          default=2,
                                          help_text="Total spots available for the contest")
    current_entries = models.PositiveIntegerField(null=False,
                                                  default=0,
                                                  help_text="The number of entries submitted to the contest")

    gpp = models.BooleanField(default=False, null=False,
                              help_text='a gpp Contest will not be cancelled if it does not fill')

    respawn = models.BooleanField(default=False, null=False,
                                  help_text='indicates whether a new identical Contest should be created when this one fills up')

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
        """
        return a QuerySet of the games which are included in the draft_group
        """
        dgm = DraftGroupManager()
        return dgm.get_games( self.draft_group )

    def save(self, *args, **kwargs):
        # if self.pk is None and not self.cid:
        #     self.cid = get_random_string(length=self.DEFAULT_CID_LENGTH)
        # super().save(*args, **kwargs)

        if self.pk is None and not self.cid:
            while True: # we'll break when we've found a non-existing id
                random_str = get_random_string(length=self.DEFAULT_CID_LENGTH)
                try:
                    Contest.objects.get( cid=random_str )
                    continue # this one existed apparently, keep trying
                except self.DoesNotExist:
                    # this one is unique!
                    #print(random_str, 'is a unique, unused searchid. lets use it.')
                    self.cid = random_str
                    break # out of while

        # set the draftgroup, if its not set
        #self.set_draftgroup_on_create()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        this method exists to support generic views ContestCreate, ContestUpdate, and ContestDelete
        """
        return reverse('contest-detail', kwargs={'pk': self.pk})

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
    lineup      = models.ForeignKey("lineup.Lineup", null=True)
    user = models.ForeignKey(User, null=False)

    def __str__(self):
        return '%s %s' % (self.contest.name, str(self.lineup))

class Action(models.Model):
    created = models.DateTimeField( auto_now_add=True)
    transaction = models.OneToOneField("transaction.Transaction",
                                    null=False,)
    contest = models.ForeignKey(Contest,
                                null=False)
    entry = models.OneToOneField(Entry,
                                 null=False)

    class Meta:
        abstract = True
