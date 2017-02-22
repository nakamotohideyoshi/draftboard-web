from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.crypto import get_random_string

from draftgroup.classes import DraftGroupManager
from sports.classes import SiteSportManager


class SkillLevel(models.Model):
    """
    Tiers:                      enforced (bool)
        veteran:    $10+        True
        rookie:     $0+         True
        all:        $0(na)      False             # special level, wont/cant/shouldnt block Entries ever

    """
    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    name = models.CharField(
        unique=True,
        max_length=32,
        null=False
    )

    gte = models.FloatField(
        default=0.0,
        null=False,
        help_text='this SkillLevel is for buyins Greater-than-or-Equal (gte) to this value.'
    )

    enforced = models.BooleanField(
        default=True,
        null=False
    )

    def __str__(self):
        return '<SkillLevel: [pk=%s]: %s, >= %s, enforced: %s>' % (
            self.pk, self.name, self.gte, self.enforced)


class AbstractContest(models.Model):
    """
    Represents all the settings, and statuses of a Contest.
    """

    DEFAULT_CID_LENGTH = 6  # the default number of characters in the contest 'cid'

    def __str__(self):
        return '<AbstractContest: pk:%s | status:%s | name:%s | start:%s | end:%s>' % (
            self.pk, self.status, self.name, self.start, self.end)

    created = models.DateTimeField(
        auto_now_add=True)

    cid = models.CharField(
        max_length=DEFAULT_CID_LENGTH,
        default='',
        null=False,
        blank=True,
        editable=False,
        help_text='unique, randomly chosen when Contest is created')

    site_sport = models.ForeignKey(
        'sports.SiteSport',
        null=False,
        related_name='%(app_label)s_%(class)s_site_sport')

    name = models.CharField(
        default="",
        null=False,
        verbose_name="Name",
        max_length=256,
        help_text="frontfacing name")

    prize_structure = models.ForeignKey(
        'prize.PrizeStructure',
        null=False)

    # start & today_only/end determine the range of time,
    # in between which live sporting events will be included
    # and players from them can be drafted
    start = models.DateTimeField(
        null=False,
        verbose_name='Start Time',
        help_text='the start should coincide with the start of a real-life game.')

    # today_only  = models.BooleanField(default=True, null=False)

    end = models.DateTimeField(
        null=False,
        blank=True,
        verbose_name='Cutoff Time',
        help_text='forces the end time of the contest (will override "Ends tonight" checkbox!!')

    # set the pool of players this contest can draft from
    draft_group = models.ForeignKey(
        'draftgroup.DraftGroup',
        null=True,
        blank=True,
        verbose_name='DraftGroup',
        help_text='the pool of draftable players and their salaries, for the games this contest includes.')

    max_entries = models.PositiveIntegerField(
        null=False,
        default=1,
        help_text="USER entry limit")

    entries = models.PositiveIntegerField(
        null=False,
        default=2,
        help_text="CONTEST limit")

    current_entries = models.PositiveIntegerField(
        null=False,
        default=0,
        help_text="The current # of entries in the contest")

    gpp = models.BooleanField(
        default=False,
        null=False,
        help_text='a gpp Contest will not be cancelled if it does not fill')

    respawn = models.BooleanField(
        default=False,
        null=False,
        help_text='indicates whether a new identical Contest should be created when this one fills up')

    doubleup = models.BooleanField(
        default=False,
        null=False,
        help_text='whether this contest has a double-up style prize structure')

    skill_level = models.ForeignKey(
        SkillLevel,
        null=False)

    def is_started(self):
        """
        used in the contest.buyin.classes.BuyinManager validation
        :return:
        """
        return timezone.now() >= self.start

    @property
    def buyin(self):
        return self.prize_structure.buyin

    @property
    def sport(self):
        return self.site_sport.name

    @property
    def prize_pool(self):
        return self.prize_structure.prize_pool

    def is_filled(self):
        """
        :return: True if there are no more entry spots left in this contest, otherwse returns False
        """
        return self.entries == self.current_entries

    def __get_game_model(self):
        ssm = SiteSportManager()
        return ssm.get_game_class(self.site_sport)

    def games(self):
        """
        return a QuerySet of the games which are included in the draft_group
        """
        dgm = DraftGroupManager()
        return dgm.get_games(self.draft_group)

    def save(self, *args, **kwargs):
        """
        override the model's save() method to keep up with some bookeepping

        :param args:
        :param kwargs:
        :return:
        """

        if 'override_entries' not in kwargs:
            self.entries = self.prize_structure.get_entries()
        else:
            kwargs.pop('override_entries')  # delete it or super() will be unhappy later

        if self.pk is None and not self.cid:
            while True:  # we'll break when we've found a non-existing id
                random_str = get_random_string(length=self.DEFAULT_CID_LENGTH)
                try:
                    self.__class__.objects.get(cid=random_str)
                    continue  # this one existed apparently, keep trying
                except self.DoesNotExist:
                    self.cid = random_str
                    break

        super().save(*args, **kwargs)

    def players(self):
        dgm = DraftGroupManager()
        return dgm.get_players(self.draft_group)

    def get_absolute_url(self):
        """
        this method exists to support generic views ContestCreate, ContestUpdate, and ContestDelete
        """
        return reverse('contest-detail', kwargs={'pk': self.pk})

    def __prepare_copy(self):
        self.pk = None
        self.cid = None
        self.current_entries = 0

    def spawn(self):
        """
        caveat: spawn() changes 'self' to the NEW contest instance!

        creates a new instance of the underlying Contest with the same
        properties, with a few notable exceptions:

            1) the current_entries is reset to zero to allow buy-ins

        """
        self.__prepare_copy()
        self.save()
        return self

    def clone(self, start, end):
        """
        create a new instance of the underlying Contest with
        nearly the same properties, but with the start & end time specified.

        clone() modified the status (resets it to scheduled).

        clone() is similar, but different than spawn().
        It may result in a new draft group being created, etc...

        by default clone() sets the 'end' property to the datetime
        which is offset by exactly as much as
        """
        self.__prepare_copy()
        self.start = start
        self.end = end
        dgm = DraftGroupManager()
        self.draft_group = dgm.get_for_contest(self)
        return self

    class Meta:
        abstract = True


class ContestPool(AbstractContest):
    # the statuses of a ContestPool
    SCHEDULED = 'scheduled'  # its upcoming
    CREATED = 'created'  # it has started, and all contests have been created
    STATUS_ALL = [
        SCHEDULED,
        CREATED,
    ]
    STATUS = (
        ('Scheduled', (
            (SCHEDULED, 'Scheduled'),  # contest pool hasnt started yet
        )),
        ('Created', (
            (CREATED, 'Created'),  # contest pool generated contests at its start time
        )),
    )

    # NOTE: contests which are created for "early registration" will
    # be set to the REGISTERING status -- and they will have a None draft_group
    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default=SCHEDULED,
        null=False)

    def __str__(self):
        return '<ContestPool: pk:%s | status:%s | name:%s | start:%s | end:%s>' % (
            self.pk, self.status, self.name, self.start, self.end)

    class Meta:
        abstract = False
        verbose_name = 'Contest Pools (All)'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        super().save(override_entries=True, *args, **kwargs)


class LobbyContestPool(ContestPool):
    """
    PROXY model for Upcoming ContestPools

    This is the model which gets the ContestPools for
    display on the home lobby, so make sure you know
    what you are doing if you are making changes.
    """

    class LobbyContestPoolManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status=ContestPool.SCHEDULED,
                                                 start__gt=timezone.now())

    objects = LobbyContestPoolManager()

    class Meta:
        proxy = True
        verbose_name = 'Contest Pools (Lobby)'
        verbose_name_plural = verbose_name


class UpcomingContestPool(ContestPool):
    """
    PROXY model for upcoming Contests ... and rest API use.

    This model contains all the ContestPools which havent started yet.

    This may appear the same as the LobbyContestPool model,
    however this should always contain all the ContestPools,
    whereas LobbyContestPool may not!
    """

    class UpcomingContestPoolManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status=ContestPool.SCHEDULED,
                                                 start__gt=timezone.now())

    # yes, the UpcomingContest.objects on which you can get() or filter(), etc...
    objects = UpcomingContestPoolManager()

    class Meta:
        proxy = True
        verbose_name = 'Upcoming'
        verbose_name_plural = 'Upcoming'


class LiveContestPool(ContestPool):
    """
    PROXY model for Live ContestPools

    Get the live ContestPool objects, which should only exist in this state
    until they have spawned the necessary Contests and have had their
    status set to 'created'.
    """

    class LiveContestPoolManager(models.Manager):
        def get_queryset(self):
            # qs = super().get_queryset()
            # now = timezone.now()
            # print('%s objects in initial QuerySet' % str(qs.count()))
            # print('ContestPool.SCHEDULED [%s]' % ContestPool.SCHEDULED,
            #        'start__lte= [%s]' % str(now))
            # qs2 = qs.filter(
            return super().get_queryset().filter(status=ContestPool.SCHEDULED,
                                                 start__lte=timezone.now())

    objects = LiveContestPoolManager()

    class Meta:
        proxy = True


class Contest(AbstractContest):
    #
    # all possible statuses
    CLONED = 'cloned'  # needs admin review and potential modifications
    RESERVABLE = 'reservable'  # far off contest you can buy into, but cannot draft a team for yet.
    SCHEDULED = 'scheduled'  # standard draftable contest before it begins
    INPROGRESS = 'inprogress'  # a live contest!
    COMPLETED = 'completed'  # the contest is over, but not yet paid out (and 'closed')
    CLOSED = 'closed'  # a paid out contest
    CANCELLED = 'cancelled'  # a non-guarantee that did not fill up, and did not run (any users were refunded)

    #
    # categories of statuses
    STATUS_UPCOMING = [
        SCHEDULED,  # scheduled first in list because its going to be the default option
        RESERVABLE
    ]

    STATUS_LIVE = [
        INPROGRESS,
        COMPLETED  # ie: needs to be paid out
    ]

    STATUS_HISTORY = [
        CLOSED,
        CANCELLED
    ]

    # combination of UPCOMING & LIVE for the main contest lobby
    STATUS_LOBBY_CONTESTS = []
    STATUS_LOBBY_CONTESTS += STATUS_UPCOMING
    # STATUS_LOBBY_CONTESTS += STATUS_LIVE

    # this status, which contains LIVE and UPCOMING contests, will be used
    # primarily for deciding which Lineups/ Entries we care about in api endpoints.
    # ... historical lineups/entries will be dealt with another way.
    STATUS_CURRENT_CONTESTS = []
    STATUS_CURRENT_CONTESTS += STATUS_UPCOMING
    STATUS_CURRENT_CONTESTS += STATUS_LIVE

    STATUS_ALL = []
    STATUS_ALL += STATUS_UPCOMING
    STATUS_ALL += STATUS_LIVE
    STATUS_ALL += STATUS_HISTORY

    #
    # group
    STATUS = (
        (
            'Upcoming', (
                (RESERVABLE, 'Reservable'),  # no players pools, but challenge can be bought into
                (SCHEDULED, 'Scheduled'),  # contest is draftable - it hasnt started yet
            )
        ),
        (
            'Live', (
                (INPROGRESS, 'In Progress'),  # game is locked, no new entries

                # the contest is ready to be paid out.
                # do not confuse this with the 'completed' status of sportradar games.
                # in the context of a Contest, 'completed' means the live games are 'closed' !!!
                (COMPLETED, 'Completed'),
            )
        ),
        (
            'History', (
                (CLOSED, 'Closed'),  # game is paid out, this is a final status
                (CANCELLED, 'Cancelled'),
                # game has been refunded, and closed. was not, and wont pay out
            )
        ),

    )

    # NOTE: contests which are created for "early registration" will
    # be set to the REGISTERING status -- and they will have a None draft_group
    status = models.CharField(max_length=32, choices=STATUS, default=INPROGRESS, null=False)

    def __str__(self):
        return '<Contest: pk:%s | status:%s | name:%s | start:%s | end:%s>' % (
            self.pk, self.status, self.name, self.start, self.end)

    class Meta:
        abstract = False

        verbose_name = 'All Contests'
        verbose_name_plural = 'All Contests'


class CurrentContest(Contest):
    """
    PROXY model for Upcoming & Live Contests ... but for which User Entries will be pulled out of.

    The reason for separating this from LobbyContest is in preparation for potential future changes.

    This is the model which gets the Contests for
    display on the home lobby, so make sure you know
    what you are doing if you are making changes.
    """

    class CurrentContestManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status__in=Contest.STATUS_CURRENT_CONTESTS)

    objects = CurrentContestManager()

    class Meta:
        proxy = True


class CompletedContest(Contest):
    """
    PROXY model for completed Contests that are not paid out ... and rest API use.

    This model has access to all contests which are completed but not paid out
    """

    class CompletedContestManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status=Contest.COMPLETED)

    # yes, the UpcomingContest.objects on which you can get() or filter(), etc...
    objects = CompletedContestManager()

    class Meta:
        proxy = True
        verbose_name = 'Completed'
        verbose_name_plural = 'Completed'


class LiveContest(Contest):
    """
    PROXY model for Live Contests ... and rest API use.

    This model can get any Contest which is currently live on the site.
    """

    class LiveContestManager(models.Manager):
        """
        Contests are considered to be in progress when its past
        the start time!
        """

        def get_queryset(self):
            now = timezone.now()
            return super().get_queryset().filter(start__lte=now).exclude(
                status__in=Contest.STATUS_HISTORY)

    objects = LiveContestManager()

    class Meta:
        proxy = True
        verbose_name = 'Live'
        verbose_name_plural = 'Live'


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
        verbose_name = 'History'
        verbose_name_plural = 'History'


class ClosedContest(Contest):
    """
    PROXY model for viewing only the Closed (paid) contests .. and rest API use.
    """

    class ClosedContestManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status=Contest.CLOSED)

    objects = ClosedContestManager()

    class Meta:
        proxy = True
        verbose_name = 'Paid Out'
        verbose_name_plural = 'Paid Out'


class Entry(models.Model):
    """
    An instance of a Lineup in a Contest (having been entered from a ContestPool starting)
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    contest = models.ForeignKey(Contest, null=True, related_name='contest_entries')
    # although this field will never be null, we allow it
    # because replays will break if it cannot be migrated easily
    contest_pool = models.ForeignKey(ContestPool, null=True, related_name='contest_pools')
    lineup = models.ForeignKey("lineup.Lineup", null=True, related_name='entries')
    user = models.ForeignKey(User, null=False)
    final_rank = models.IntegerField(
        default=-1, null=False,
        help_text='the rank of the entry after the contest has been paid out'
    )

    def __str__(self):
        return ('<Entry: user:%s | lineup:%s | rank:%s | created:%s '
                '\n\tcontest_pool:%s \n\tcontest:%s>') % (
                   self.user, self.lineup, self.final_rank, self.created, self.contest_pool,
                   self.contest)

    class Meta:
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'


class CurrentEntry(Entry):
    """
    PROXY model for Upcoming & Live Entry objects.

    includes Entry objects from the no-mans-land time between start of ContestPool and Contest creation
    """

    class CurrentEntryManager(models.Manager):
        def get_queryset(self):
            # entries = Entry.objects.filter(Q(user__username='user1'), Q(contest__isnull=True) | Q(contest__in=LiveContest.objects.all()))
            return super().get_queryset().filter(Q(contest__isnull=True) |
                                                 Q(contest__in=LiveContest.objects.all()))

    objects = CurrentEntryManager()

    class Meta:
        proxy = True


class HistoryEntry(Entry):
    """
    PROXY model for viewing only the Historical entries .. and rest API use.
    """

    class HistoryEntryManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(contest__in=HistoryContest.objects.all())

    objects = HistoryEntryManager()

    class Meta:
        proxy = True


class ClosedEntry(Entry):
    """
    PROXY model for viewing only the Closed (paid out) entries ... and rest API use.
    """

    class ClosedEntryManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(contest__in=ClosedContest.objects.all())

    objects = ClosedEntryManager()

    class Meta:
        proxy = True


class Action(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    transaction = models.OneToOneField("transaction.Transaction", null=False)
    contest = models.ForeignKey(Contest, null=True)

    class Meta:
        abstract = True

    @property
    def user(self):
        return self.transaction.user

    def to_json(self):
        return {"created": str(self.created), "contest": self.contest.pk,
                "type": self.__class__.__name__,
                "id": self.pk}
