from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from pytz import timezone as pytz_timezone


class Block(models.Model):
    """ a sport and a time, which characterizes a ContestPools start time """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    site_sport = models.ForeignKey('sports.SiteSport', null=False)
    dfsday_start = models.DateTimeField(null=False)
    dfsday_end = models.DateTimeField(null=False)
    cutoff_time = models.TimeField(null=False)
    cutoff = models.DateTimeField(null=False, blank=True,
                                  help_text='the UTC datetime object for the cutoff_time')
    # A flag that will disable the automatic spawning of contest pools.
    # This is useful if you are manually creating a Block in the admin section but
    # don't want it to immediately spawn contest pools when you save.
    should_create_contest_pools = models.BooleanField(
        default=True,
        help_text='If this is checked, the contest pool creator will not spawn contest pools! '
                    'You should check this until you are sure all necessary games and prize '
                    'structures are included.'
    )
    # False if the ContestPools for this Block have not been created yet.
    # otherwise, this field should be set to True if ANY Contest Pools have been created
    contest_pools_created = models.BooleanField(default=False)

    class Meta:
        unique_together = ('site_sport', 'dfsday_start', 'dfsday_end', 'cutoff_time')

    def __str__(self):
        local_cutoff = self.get_utc_cutoff().astimezone(pytz_timezone(settings.TIME_ZONE))
        return '<Block id: %s | sport: %s | local_cutoff: %s>' % (self.pk, self.site_sport, str(local_cutoff))

    def save(self, *args, **kwargs):
        """
        override save() method to update the cutoff datetime
        """
        self.cutoff = self.get_utc_cutoff()
        super().save(*args, **kwargs)

    def get_utc_cutoff(self):
        """
        we have to convert the dfsday start to local time (EST), combine
        with the time object, and convert it back to UTC so we can
        compare it with the games in the database, which are in UTC !
        """

        # convert the utc start of the day into est  (so should be 00:00:01 AM basically)
        est_startofday = self.dfsday_start.astimezone(pytz_timezone(settings.TIME_ZONE))
        year = est_startofday.year
        month = est_startofday.month
        day = est_startofday.day
        hour = self.cutoff_time.hour
        minute = self.cutoff_time.minute
        #                                                          ms, microsec
        est_cutoff = est_startofday.replace(year, month, day, hour, minute, 0, 0)
        utc_cutoff = est_cutoff.astimezone(pytz_timezone('UTC'))
        # print('cutoff_time:', str(self.cutoff_time), 'utc_cutoff', str(utc_cutoff))
        return utc_cutoff

    def get_block_games(self):
        """
        returns a tuple of two lists in the form: ([included games], [excluded games])
        """
        included = []
        excluded = []
        utc_cutoff = self.get_utc_cutoff()

        for block_game in BlockGame.objects.filter(block=self):
            if block_game.game.start < utc_cutoff:
                excluded.append(block_game)
            else:
                included.append(block_game)
        #
        # return a tuple of included, excluded
        return included, excluded


class UpcomingBlock(Block):
    """ PROXY for upcoming Blocks """

    class UpcomingBlockManager(models.Manager):
        def get_queryset(self):
            # allegedly order_by() can take multiple params to sort by
            return super().get_queryset().filter(
                cutoff__gte=timezone.now()).order_by('dfsday_start', 'cutoff_time')

        def get_tomorrow_blocks(self):
            return super().get_queryset().filter(
                cutoff__date__in=[timezone.now().date(),
                                  timezone.now().date() + timezone.timedelta(days=1)]).order_by(
                'dfsday_start', 'cutoff_time')

    objects = UpcomingBlockManager()

    class Meta:
        proxy = True
        verbose_name = 'Schedule'


class DefaultPrizeStructure(models.Model):
    """ for a sport, this is the set of PrizeStructures to create for a Block """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    site_sport = models.ForeignKey('sports.SiteSport', null=False)
    prize_structure = models.ForeignKey('prize.PrizeStructure', null=False)

    class Meta:
        unique_together = ('site_sport', 'prize_structure')

    def __str__(self):
        return '%s - %s' % (self.site_sport, self.prize_structure)


class BlockGame(models.Model):
    """ an object that maps a real life game to a block """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=256, null=False, blank=False, default='')
    block = models.ForeignKey('schedule.Block', null=False)
    srid = models.CharField(max_length=128, null=False)
    game_type = models.ForeignKey(
        ContentType)  # ,  related_name='%(app_label)s_%(class)s_block_game')
    game_id = models.PositiveIntegerField()
    game = GenericForeignKey('game_type', 'game_id')

    class Meta:
        unique_together = ('block', 'srid')

    def __str__(self):
        return "<BlockGame id: %s - game: %s>" % (self.id, self.game)

class BlockPrizeStructure(models.Model):
    """ for a block, this is the editable set of PrizeStructures (editable until the block starts) """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    block = models.ForeignKey('schedule.Block', null=False)
    prize_structure = models.ForeignKey('prize.PrizeStructure', null=False)

    def __str__(self):
        return '%s - %s' % (self.block, self.prize_structure)

    class Meta:
        unique_together = ('block', 'prize_structure')
