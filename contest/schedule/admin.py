#
# contest/schedule/admin.py

from django.contrib import admin
from django.contrib.admin.widgets import AdminSplitDateTime
from django.utils.html import format_html
import contest.schedule.models
import contest.schedule.forms

@admin.register(contest.schedule.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['created','name']

@admin.register(contest.schedule.models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['created','modified','site_sport','category','enable']

@admin.register(contest.schedule.models.TemplateContest)
class TemplateContestAdmin(admin.ModelAdmin):

    # list_display = [
    #     'site_sport',
    #     'name',
    #     'prize_structure',
    # ]

    # from django.utils.html import format_html
    # def colored_first_name(self):
    #     return format_html('<span style="color: #{};">{}</span>',
    #                        self.color_code,
    #                        self.first_name)

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
        ('Scheduled Contest Template', {
            'fields': (
                'site_sport',
                'name',

                'prize_structure',
                'max_entries',
                'entries',

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
    ]
