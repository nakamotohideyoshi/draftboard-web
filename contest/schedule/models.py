#
# contest/schedule/models.py

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
import contest.models
from prize.models import (
    PrizeStructure,
)
from django.conf import settings
from django.utils import timezone
from pytz import timezone as pytz_timezone

class Notification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=128, null=False, unique=True)
    enabled = models.BooleanField(default=True, null=False)
    # TODO are there more fields?
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
    class Meta:
        unique_together = ('site_sport','dfsday_start','dfsday_end','cutoff_time')
    def __str__(self):
        local_cutoff = self.get_utc_cutoff().astimezone(pytz_timezone(settings.TIME_ZONE))
        return '%s %s' % (self.site_sport, str(local_cutoff))
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
        #print('cutoff_time:', str(self.cutoff_time), 'utc_cutoff', str(utc_cutoff))
        return utc_cutoff
    def get_block_games(self):
        """
        returns a tuple of two lists in the form: ([included games], [excluded games])

        :param block:
        :return:
        """
        included    = []
        excluded    = []
        utc_cutoff  = self.get_utc_cutoff()

        for block_game in BlockGame.objects.filter(block=self):
            if block_game.game.start < utc_cutoff:
                excluded.append(block_game)
            else:
                included.append(block_game)
        #
        # return a tuple of included, excluded
        return (included, excluded)
    # TODO finish implementing
class UpcomingBlock(Block):
    """ PROXY for upcoming Blocks """
    class UpcomingBlockManager(models.Manager):
        def get_queryset(self):
            # allegedly order_by() can take multiple params to sort by
            return super().get_queryset().filter(
                cutoff__gte=timezone.now()).order_by('dfsday_start','cutoff_time')
    objects = UpcomingBlockManager()
    class Meta:
        proxy = True
        verbose_name = 'Schedule'
    # TODO finish implementing
class DefaultPrizeStructure(models.Model):
    """ for a sport, this is the set of PrizeStructures to create for a Block """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    site_sport = models.ForeignKey('sports.SiteSport', null=False)
    prize_structure = models.ForeignKey('prize.PrizeStructure', null=False)
    class Meta:
        unique_together = ('site_sport','prize_structure')
    # TODO finish implementing
class BlockGame(models.Model):
    """ an object that maps a real life game to a block """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=256, null=False, blank=False, default='')
    block = models.ForeignKey('schedule.Block', null=False)
    srid = models.CharField(max_length=128, null=False)
    game_type           = models.ForeignKey(ContentType) #,  related_name='%(app_label)s_%(class)s_block_game')
    game_id             = models.PositiveIntegerField()
    game                = GenericForeignKey('game_type', 'game_id')
    class Meta:
        unique_together = ('block','srid')
# class IncludedBlockGame(BlockGame):
#     """ PROXY for "included" block games """
#     class IncludedBlockGameManager(models.Manager):
#         def get_queryset(self):
#             return super().get_queryset().filter()
#     objects = IncludedBlockGameManager()
#     class Meta:
#         proxy = True
class BlockPrizeStructure(models.Model):
    """ for a block, this is the editable set of PrizeStructures (editable until the block starts) """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    block = models.ForeignKey('schedule.Block', null=False)
    prize_structure = models.ForeignKey('prize.PrizeStructure', null=False)
    class Meta:
        unique_together = ('block','prize_structure')
    # TODO finish implementing

class Category( models.Model ):
    created     = models.DateTimeField(auto_now_add=True)
    name        = models.CharField(max_length=128, null=False)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Time Slot'


class Schedule( models.Model ):
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    site_sport  = models.ForeignKey( 'sports.SiteSport', null=False )
    category    = models.ForeignKey( Category, null=False )
    enable      = models.BooleanField(default=False, null=False,
                                      help_text='if enable=True, the scheduler should be creating Contests for this schedule!')

    class Meta:
        unique_together = ('site_sport', 'category')

    def __str__(self):
        if self.enable:
            enabled = '*Active*'
        else:
            enabled = 'Disabled'
        return '[ %s ] %s - %s' % (enabled, self.site_sport.name, self.category.name)

class TemplateContest( contest.models.AbstractContest ):
#class TemplateContest( contest.models.Contest ):
    """
    a Contest - for all intents and purposes - just in a different table,
    and used by the scheduler.

    fields that will never be used and can be ignored from its parent:
        -> start, end, draft_group, current_entries
    """

    # since we are not adding any properties, this makes sure
    # the model's table gets created properly

    def __str__(self):
        return self.name

    class Meta:
        abstract = False
        verbose_name = 'Contest Template'


class Interval(models.Model):

    monday      = models.BooleanField(default=False, null=False)
    tuesday     = models.BooleanField(default=False, null=False)
    wednesday   = models.BooleanField(default=False, null=False)
    thursday    = models.BooleanField(default=False, null=False)
    friday      = models.BooleanField(default=False, null=False)
    saturday    = models.BooleanField(default=False, null=False)
    sunday      = models.BooleanField(default=False, null=False)

    def __str__(self):
        days = []
        if self.monday:     days.append('Mon')
        if self.tuesday:    days.append('Tue')
        if self.wednesday:  days.append('Wed')
        if self.thursday:   days.append('Thu')
        if self.friday:     days.append('Fri')
        if self.saturday:   days.append('Sat')
        if self.sunday:     days.append('Sun')

        days_str = '*%s* ' % str(len(days))
        return days_str +  '|'.join(days)

class ScheduledTemplateContest( models.Model ):
    """
    this is the contest we will try to schedule when the time comes

    we override save() because this model inherits from Contest,
    however we do not care about all the fields (ie: start / end)
    """

    schedule            = models.ForeignKey(Schedule, null=False,
                            help_text='the main schedule this template is associated with')
    template_contest    = models.ForeignKey(TemplateContest, null=False,
                            help_text='this is the contest the scheduler will create when the time comes')
    start_time          = models.TimeField(null=False,
                            help_text='the time the scheduled contest should begin. ie: 19:00:00 ... (thats 7:00 PM)')
    duration_minutes    = models.IntegerField(default=0, null=False,
                            help_text='so we can calculate the end time. end_time = (start_time + timedelta(minutes=duration_minutes)).')

    interval            = models.ForeignKey(Interval, null=False)

    multiplier          = models.IntegerField(default=1, null=False,
                            help_text='the number of copies of this contest to create (ie: you might want ten 1v1 contests of the same type active at the same time)')
    class Meta:
        unique_together = ('schedule','template_contest','start_time','duration_minutes')
        verbose_name= 'Master Schedule'

    def __str__(self):
        return '%s    days:%s    Contest >>>>> %s    schedule id:%s' % (self.start_time,
                                            self.interval, self.template_contest, self.pk)
#
# UNCOMMENT THIS AND MAKE THIS BE THE HISTORY ROW FOR EACH TIME WE CREATE A NEW CONTEST BEAUSE OF THE SCHEDULE
#
class CreatedContest( models.Model ):
    """
    This model should be created atomically with whatever actual Contest is being created!

    a record of a contest that was created because of the scheduler.
    has references to the template, and the contest that was created.
    """

    created             = models.DateTimeField(auto_now_add=True)

    day                 = models.DateField(null=False)
    scheduled_template_contest   = models.ForeignKey(ScheduledTemplateContest, null=False, related_name='scheduled_contest_history_item')
    contest             = models.ForeignKey('contest.Contest', null=False, related_name='scheduled_contest_contest')

    def __str__(self):
        return '%s %s    %s    schedule id:%s' % (self.day, self.contest.start,
                                                self.contest.name,
                                                self.scheduled_template_contest.pk)