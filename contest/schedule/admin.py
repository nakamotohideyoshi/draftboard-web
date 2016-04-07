#
# contest/schedule/admin.py

from django.conf import settings
from pytz import timezone
from django.contrib import admin
from django.contrib.admin.widgets import AdminSplitDateTime
from django.contrib.contenttypes import generic
from django.utils.html import format_html
import contest.schedule.models
import contest.schedule.forms

#
# WARNING: this sets en_formats for ALL contest.schedule admin model fields!
from django.conf.locale.en import formats as en_formats
en_formats.DATETIME_FORMAT = "l, M P"

#
#DATETIME_FORMAT = '%A, %d. %B %Y %I:%M%p'    # %B %Y is MM YYYY
WKDAY   = '%A'
DAYNUM  = '%d'      # ie: 15 means the 15th day of the month
MONTH   = '%B'
YEAR    = '%Y'
TIMEPM  = '%I:%M %p'

WEEKDAY_FORMAT = WKDAY
DATE_FORMAT = WEEKDAY_FORMAT + ', ' + DAYNUM
TIME_FORMAT = TIMEPM
MONTH_FORMAT = MONTH
WEEKDAY_MONTH_FORMAT = WEEKDAY_FORMAT + ', ' + MONTH + ' ' + DAYNUM
WEEKDAY_TIME_FORMAT = WEEKDAY_FORMAT + ', ' + TIME_FORMAT
WEEKDAY_MONTH_TIME_FORMAT = '%s, %s %s. %s' % (WEEKDAY_FORMAT, MONTH_FORMAT, DAYNUM, TIME_FORMAT)

def as_local_timezone(datetime_obj):
    return datetime_obj.astimezone(timezone(settings.TIME_ZONE))

def local_date(datetime_obj):
    #dt = datetime_obj.astimezone(timezone(settings.TIME_ZONE))
    dt = as_local_timezone(datetime_obj)
    return dt.strftime(DATE_FORMAT)

def local_time(datetime_obj):
    #dt = datetime_obj.astimezone(timezone(settings.TIME_ZONE))
    dt = as_local_timezone(datetime_obj)
    return dt.strftime(TIME_FORMAT)

def local_daytime(datetime_obj):
    #dt = datetime_obj.astimezone(timezone(settings.TIME_ZONE))
    dt = as_local_timezone(datetime_obj)
    return dt.strftime(WEEKDAY_TIME_FORMAT)

def local_daymonth(datetime_obj):
    #dt = datetime_obj.astimezone(timezone(settings.TIME_ZONE))
    dt = as_local_timezone(datetime_obj)
    return dt.strftime(WEEKDAY_MONTH_FORMAT)

def local_daymonthtime(datetime_obj):
    #dt = datetime_obj.astimezone(timezone(settings.TIME_ZONE))
    dt = as_local_timezone(datetime_obj)
    return dt.strftime(WEEKDAY_MONTH_TIME_FORMAT)

class TabularInlineBlockGame(admin.TabularInline):

    block_obj = None  # for children Included, Excluded versions

    model = contest.schedule.models.BlockGame
    extra = 3

    readonly_fields = ('game_start_time_est', 'name')
    exclude = ('srid', 'game_id', 'game_type', 'game')

    def date_est(self, obj):
        dt = local_date(obj.game.start)
        print(str(dt))
        return dt

    def game_start_time_est(self, obj):
        dt = local_daymonthtime(obj.game.start)
        print(str(dt))
        return dt

    # def get_queryset(self, request):
    #     print(str(request))
    #     return super().get_queryset(request)

    def get_extra(self, request, obj=None, **kwargs):
        """Dynamically sets the number of extra forms. 0 if the related object
        already exists or the extra configuration otherwise."""
        if obj:
            # Don't add any extra forms if the related object already exists.
            return 0
        return self.extra

    def set_block_obj(self, block_obj):
        self.block_obj = block_obj

class TabularInlineBlockGameIncluded(TabularInlineBlockGame):

    def get_queryset(self, request):
        """ get included blocks """
        included, excluded = self.block_obj.get_block_games()
        qs = super().get_queryset(request)
        print('block?', str(self.block_obj), 'qs:', str(qs))
        included_game_block_ids = [ g.pk for g in included ]
        qs = qs.filter(pk__in=included_game_block_ids)
        return qs

class TabularInlineBlockGameExcluded(TabularInlineBlockGame):

    def get_queryset(self, request):
        """ get excluded blocks """
        included, excluded = self.block_obj.get_block_games()
        qs = super().get_queryset(request)
        print(str(qs))
        excluded_game_block_ids = [ g.pk for g in excluded ]
        qs = qs.filter(pk__in=excluded_game_block_ids)
        return qs

class TabularInlineBlockPrizeStructure(admin.TabularInline):

    model = contest.schedule.models.BlockPrizeStructure
    extra = 3

    def get_extra (self, request, obj=None, **kwargs):
        """Dynamically sets the number of extra forms. 0 if the related object
        already exists or the extra configuration otherwise."""
        if obj:
            # Don't add any extra forms if the related object already exists.
            return 0
        return self.extra

@admin.register(contest.schedule.models.Block)
class BlockAdmin(admin.ModelAdmin):

    # customize the template, basically so we can group blocks by a Date
    # and then only show the TIME in the each row.
    # this template can be found in: contest/schedule/templates/admin/change_list.html

    #change_list_template = 'change_list_block.html'

    list_display = ['sport','weekday','games_included','earliest_game_in_block','cutoff_time']
    list_filter = ['site_sport',]
    list_editable = ['cutoff_time',]
    ordering = ('dfsday_start','site_sport')

    block_game_inlines = [
        TabularInlineBlockGameIncluded,
        TabularInlineBlockGameExcluded,
    ]
    inlines = [
        # TabularInlineBlockGameIncluded,
        # TabularInlineBlockGameExcluded,
        TabularInlineBlockPrizeStructure,
    ]

    def sport(self, obj):
        return obj.site_sport.name.upper()

    def weekday(self, obj):
        return local_daymonth(obj.dfsday_start)

    def cutoff_time(self, obj):
        return local_time(obj.dfsday_start)

    # def get_changelist_form(self, request, **kwargs):
    #     kwargs.setdefault('form', MyAdminForm)
    #     return super(MyModelAdmin, self).get_changelist_form(request, **kwargs)

    # def __get_utc_cutoff(self, block):
    #     """
    #     we have to convert the dfsday start to local time (EST), combine
    #     with the time object, and convert it back to UTC so we can
    #     compare it with the games in the database, which are in UTC !
    #     """
    #
    #     # convert the utc start of the day into est  (so should be 00:00:01 AM basically)
    #     est_startofday = as_local_timezone(block.dfsday_start)
    #     year = est_startofday.year
    #     month = est_startofday.month
    #     day = est_startofday.day
    #     hour = block.cutoff_time.hour
    #     minute = block.cutoff_time.minute
    #     #                                                          ms, microsec
    #     est_cutoff = est_startofday.replace(year, month, day, hour, minute, 0, 0)
    #     utc_cutoff = est_cutoff.astimezone(timezone('UTC'))
    #     print('cutoff_time:', str(block.cutoff_time), 'utc_cutoff', str(utc_cutoff))
    #     return utc_cutoff

    # def get_block_games(self, block):
    #     """
    #     returns a tuple of two lists in the form: ([included games], [excluded games])
    #
    #     :param block:
    #     :return:
    #     """
    #     included    = []
    #     excluded    = []
    #     utc_cutoff  = block.get_utc_cutoff()
    #
    #     for block_game in contest.schedule.models.BlockGame.objects.filter(block=block):
    #         if block_game.game.start < utc_cutoff:
    #             excluded.append(block_game)
    #         else:
    #             included.append(block_game)
    #     #
    #     # return a tuple of included, excluded
    #     return (included, excluded)

    def get_block_games(self, block):
        return block.get_block_games()

    def earliest_game_in_block(self, block):
        """
        get the start datetime of the EARLIEST GAME CURRENTLY INCLUDED IN THE BLOCK
        """
        earliest_game = None
        included, excluded = block.get_block_games()
        for block_game in included:
            game = block_game.game
            if earliest_game is None or game.start < earliest_game.start:
                earliest_game = game
        #
        # return the localized time for the admin to display
        return local_time(earliest_game.start)

    def games_included(self, block):
        included, excluded = block.get_block_games()
        incl = len(included)
        total = incl + len(excluded)
        return '%s of %s' % (str(incl), str(total))

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []
        else:
            ret_list = []
            for inline in self.block_game_inlines:
                i = inline(self.model, self.admin_site)
                i.set_block_obj( obj )
                ret_list.append( i  )
            # add regular inlines
            ret_list.extend( [inline(self.model, self.admin_site) for inline in self.inlines] )
            return ret_list

@admin.register(contest.schedule.models.DefaultPrizeStructure)
class DefaultPrizeStructureAdmin(admin.ModelAdmin):
    list_display = ['site_sport','prize_structure']

@admin.register(contest.schedule.models.BlockPrizeStructure)
class BlockPrizeStructureAdmin(admin.ModelAdmin):
    list_display = ['block','prize_structure']

@admin.register(contest.schedule.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(contest.schedule.models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['site_sport','category','enable']

@admin.register(contest.schedule.models.TemplateContest)
class TemplateContestAdmin(admin.ModelAdmin):

    list_display = [
        'site_sport',
        'name',
        'scheduler',
    ]

    def scheduler(self, obj):
        """
        Add a button into the admin views so its easy to add a TemplateSchedule to an existing schedule

        :param obj:   the model instance for each row
        :return:
        """

        # the {} in the first argument are like %s for python strings,
        # and the subsequent arguments fill the {}
        return format_html('<a href="{}={}" class="btn btn-success">{}</a>',
                            "/admin/schedule/scheduledtemplatecontest/add/?template_contest",
                             obj.pk,
                             'Add to Schedule')

    form = contest.schedule.forms.TemplateContestForm

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = contest.schedule.forms.TemplateContestFormAdd
        return super().get_form(request, obj, **kwargs)

    #@transaction.atomic
    def save_model(self, request, obj, form, change):
        """
        Override save_model to hook up draftgroup and anything else
        we can do dynamically without forcing user to do it manually.

        :param request: http request with authenticated user
        :param obj: the model instance about to be saved
        :param form:
        :param change:
        :return:
        """
        obj.save()

    # use the fields which we are explicity stating in the Meta class
    fieldsets = (
        #
        ('Contest Template', {
            'fields': (
                'site_sport',
                'name',

                'prize_structure',
                'max_entries',

                'gpp',
                'respawn',
                'doubleup'
            )
        }),

        #
        # these fields are purposely collapsed,
        # and the form takes care of setting
        # them to default values.
        ('ignore these fields', {
            'classes' : ('collapse',),
            'fields': (
                'start',
                'end',
            )
        }),
    )

@admin.register(contest.schedule.models.ScheduledTemplateContest)
class ScheduledTemplateContestAdmin(admin.ModelAdmin):

    list_display = [
        'schedule',
        'template_contest',
        'start_time',
        'duration_minutes',
        'multiplier',
        'buyin'
    ]

    def buyin(self, obj):
        return obj.template_contest.prize_structure.generator.buyin

@admin.register(contest.schedule.models.Interval)
class IntervalAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
       """
       Return empty perms dict thus hiding the model from admin index.
       """
       return {}

    list_display = [
        'monday','tuesday','wednesday','thursday','friday','saturday','sunday'
    ]