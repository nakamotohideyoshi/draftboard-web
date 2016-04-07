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

#DATETIME_FORMAT = '%A, %d. %B %Y %I:%M%p'    # %B %Y is MM YYYY
DATETIME_FORMAT = '%A, %d. %I:%M%p'

def local_time(datetime_obj):
    dt = datetime_obj.astimezone(timezone(settings.TIME_ZONE))
    return dt.strftime(DATETIME_FORMAT)

class TabularInlineBlockGame(admin.TabularInline):

    model = contest.schedule.models.BlockGame
    extra = 3

    readonly_fields = ('start_time_est', 'name')
    exclude = ('srid', 'game_id', 'game_type', 'game')

    def start_time_est(self, obj):
        dt = local_time(obj.game.start)
        print(str(dt))
        return dt

    def get_queryset(self, request):
        print(str(request))
        return super().get_queryset(request)

    def get_extra (self, request, obj=None, **kwargs):
        """Dynamically sets the number of extra forms. 0 if the related object
        already exists or the extra configuration otherwise."""
        if obj:
            # Don't add any extra forms if the related object already exists.
            return 0
        return self.extra

class TabularInlineBlockPrizeStructure(admin.TabularInline):

    model = contest.schedule.models.BlockPrizeStructure
    extra = 3

    def get_queryset(self, request):
        print(str(request))
        return super().get_queryset(request)

    def get_extra (self, request, obj=None, **kwargs):
        """Dynamically sets the number of extra forms. 0 if the related object
        already exists or the extra configuration otherwise."""
        if obj:
            # Don't add any extra forms if the related object already exists.
            return 0
        return self.extra

@admin.register(contest.schedule.models.Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ['site_sport','start','included']
    list_filter = ['site_sport','start']
    ordering = ('start',)
    inlines = [ TabularInlineBlockGame, TabularInlineBlockPrizeStructure ]

    # TODO - the GLOBAL replayer/admin.py datetime format still takes over here
    def start(self, obj):
        return local_time(obj.start)

    # TODO - included is the total right now, not the # of included
    def included(self, obj):
        # contest.schedule.models.BlockGame.objects.
        #print('included', str(type(obj)))
        block_games = contest.schedule.models.BlockGame.objects.filter(block=obj)
        return block_games.count()

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []
        else:
            return [inline(self.model, self.admin_site) for inline in self.inlines]


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