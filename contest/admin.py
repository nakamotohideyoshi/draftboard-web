#
# contest/admin.py

from django.db import transaction
from django.contrib import admin
import contest.models
import contest.forms
from .payout.tasks import payout_task
CONTEST_LIST_DISPLAY = ['created','status','name','start','end']

@admin.register(contest.models.Contest)
class ContestAdmin(admin.ModelAdmin):
    """
    Note to programmer:
        - the clean()'ing (ie: field validation) is done in contest.forms.ContestForm
        - the post-processing, like setting the proper draft group is done in this class

    Administratively create a contest.
    """

    #list_display = CONTEST_LIST_DISPLAY
    form = contest.forms.ContestForm

    # create some "sections" of the form"
    # fieldsets = (
    #     # ('Create Contest from Existing', {
    #     #     'classes': ('collapse',),
    #     #     'fields': ('clone_from', 'name')
    #     # }),
    #
    #
    #
    #     ('Create Contest', {
    #         #'classes': ('collapse',),
    #         'fields': (
    #             'site_sport',
    #             'name',
    #             'prize_structure',
    #             'start',
    #             #'ends_tonight'
    #         )
    #     }),
    #
    #     ('Custom End Time', {
    #         'classes': ('collapse',),
    #         'fields': (
    #             'end',
    #         )
    #     }),
    # )

    # def get_form(self, request, obj=None, **kwargs):
    #     if obj is None:
    #         return contest.forms.ContestFormAdd
    #     else:
    #         return contest.forms.ContestForm(request, obj, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = contest.forms.ContestFormAdd
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


@admin.register(contest.models.UpcomingContest)
class UpcomingContestAdmin(admin.ModelAdmin):
    list_display = CONTEST_LIST_DISPLAY


@admin.register(contest.models.CompletedContest)
class CompletedContestAdmin(admin.ModelAdmin):
    list_display = CONTEST_LIST_DISPLAY

    def payout_contests(self, request, queryset):
        arr = []
        for obj in queryset:
            arr.append(obj)
        if arr == []:
            arr = None
        payout_task.delay(contests=arr)
        self.message_user(request, 'Contest Payout started. ')

    #
    # add these actions this modeladmin's view
    actions = [ payout_contests ]


@admin.register(contest.models.LiveContest)
class LiveContestAdmin(admin.ModelAdmin):
    list_display = CONTEST_LIST_DISPLAY


@admin.register(contest.models.HistoryContest)
class HistoryContestAdmin(admin.ModelAdmin):
    list_display = CONTEST_LIST_DISPLAY


@admin.register(contest.models.Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['created','updated','contest','lineup']