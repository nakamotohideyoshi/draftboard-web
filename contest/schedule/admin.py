#
# contest/schedule/admin.py

from django.conf import settings
from django.utils import timezone
from pytz import timezone as pytz_timezone
from django.contrib import admin
from django.contrib.admin.widgets import AdminSplitDateTime
from django.contrib.contenttypes import generic
from django.utils.html import format_html
import contest.schedule.classes
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
    return datetime_obj.astimezone(pytz_timezone(settings.TIME_ZONE))

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

    def has_delete_permission(self, request, obj=None):
        return False

    def date_est(self, obj):
        dt = local_date(obj.game.start)
        #print(str(dt))
        return dt

    def game_start_time_est(self, obj):
        dt = local_daymonthtime(obj.game.start)
        #print(str(dt))
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

    verbose_name = 'Included Game'
    verbose_name_plural = verbose_name + 's'

    def get_queryset(self, request):
        """ get included blocks """
        included, excluded = self.block_obj.get_block_games()
        qs = super().get_queryset(request)
        #print('block?', str(self.block_obj), 'qs:', str(qs))
        included_game_block_ids = [ g.pk for g in included ]
        qs = qs.filter(pk__in=included_game_block_ids)
        return qs

class TabularInlineBlockGameExcluded(TabularInlineBlockGame):

    verbose_name = 'Excluded Game'
    verbose_name_plural = verbose_name + 's'

    def get_queryset(self, request):
        """ get excluded blocks """
        included, excluded = self.block_obj.get_block_games()
        qs = super().get_queryset(request)
        #print(str(qs))
        excluded_game_block_ids = [ g.pk for g in excluded ]
        qs = qs.filter(pk__in=excluded_game_block_ids)
        return qs

class TabularInlineBlockPrizeStructure(admin.TabularInline):

    verbose_name = 'Contest Pool Prize Structure'
    verbose_name_plural = verbose_name + 's'
    model = contest.schedule.models.BlockPrizeStructure
    extra = 3

    def get_extra (self, request, obj=None, **kwargs):
        """Dynamically sets the number of extra forms. 0 if the related object
        already exists or the extra configuration otherwise."""
        if obj:
            # Don't add any extra forms if the related object already exists.
            return 0
        return self.extra

# @admin.register(contest.schedule.models.Block)
@admin.register(contest.schedule.models.UpcomingBlock)
class UpcomingBlockAdmin(admin.ModelAdmin):

    # customize the template, basically so we can group blocks by a Date
    # and then only show the TIME in the each row.
    # this template can be found in: contest/schedule/templates/admin/change_list.html

    #change_list_template = 'change_list_block.html'

    list_display = ['sport','weekday','games_included','earliest_game_in_block','cutoff_time']
    list_filter = ['site_sport',]
    list_editable = ['cutoff_time',]
    readonly_fields = ('site_sport',)
    exclude = ('dfsday_start','dfsday_end','cutoff')
    ordering = ('dfsday_start','site_sport')
    actions = ['create_contest_pools']

    block_game_inlines = [
        TabularInlineBlockGameIncluded,
        TabularInlineBlockGameExcluded,
    ]
    inlines = [
        # TabularInlineBlockGameIncluded,
        # TabularInlineBlockGameExcluded,
        TabularInlineBlockPrizeStructure,
    ]

    def __is_block_drafting(self, block):
        # True if there are no blocks previous to it, for its sport
        return self.model.objects.filter(cutoff__lt=block.cutoff,
                                     site_sport=block.site_sport).count() == 0

    def create_contest_pools(self, request, queryset):
        if queryset.count() != 1:
            # you must select exactly 1 block
            return
        block = queryset[0]
        if not self.__is_block_drafting(block):
            # this is not the drafting
            return
        else:
            # create the contest pools for this block manually
            cpsm = contest.schedule.classes.ContestPoolScheduleManager(block.site_sport.name)
            cpsm.create_contest_pools(block)

    def sport(self, obj):
        return obj.site_sport.name.upper()

    def weekday(self, block):
        """
        lets be specific, and if the current time is after the cutoff
        display that its running...
        """
        if self.model.objects.filter(cutoff__lt=block.cutoff,
                                     site_sport=block.site_sport).count() == 0:
            # this is the currently upcoming,
            # and there are no upcomingblocks before it,
            # which means its the active block.
            # If its ContestPools exist, they are drafting right now...
            return 'Drafting'
        return local_daymonth(block.dfsday_start)

    def cutoff_time(self, obj):
        return local_time(obj.dfsday_start)

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
        if earliest_game is None:
            return 'na'
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
    list_filter = ['site_sport',]

# @admin.register(contest.schedule.models.BlockPrizeStructure)
# class BlockPrizeStructureAdmin(admin.ModelAdmin):
#     list_display = ['block','prize_structure']

@admin.register(contest.schedule.models.Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = ['name','enabled']

    def has_delete_permission(self, request, obj=None):
        return False