#
# contest/schedule/models.py

from django.db import models
import contest.models


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