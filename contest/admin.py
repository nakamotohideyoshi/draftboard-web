#
# contest/admin.py

from django.db import transaction
from django.contrib import admin
import contest.models
import contest.forms
from contest.refund.tasks import refund_task
from .payout.tasks import payout_task
from django.utils.html import format_html

CONTEST_LIST_DISPLAY = ['name', 'created','status','start','end']

@admin.register(contest.models.Contest)
class ContestAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_display = CONTEST_LIST_DISPLAY

    def get_readonly_fields(self, request, obj=None):
        if obj:
            arr = [f.name for f in self.model._meta.fields]
            return arr
        return []

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(contest.models.UpcomingContest)
class UpcomingContestAdmin(admin.ModelAdmin):
    readonly_fields = ['entries']
    form =contest.forms.ContestFormAdd
    list_display = CONTEST_LIST_DISPLAY

    def cancel_and_refund_upcoming_contests(self, request, queryset):
        if queryset.count() > 0:
            for contest in queryset:
                refund_task.delay( contest, force=True )

    actions = [ cancel_and_refund_upcoming_contests ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            arr = [f.name for f in self.model._meta.fields]
            return arr
        return []

    """
    Note to programmer:
        - the clean()'ing (ie: field validation) is done in contest.forms.ContestForm
        - the post-processing, like setting the proper draft group is done in this class

    Administratively create a contest.
    """
    exclude = ('contest',)
    #list_display = CONTEST_LIST_DISPLAY

    #create some "sections" of the form"
    fieldsets = (
        # ('Create Contest from Existing', {
        #     'classes': ('collapse',),
        #     'fields': ('clone_from', 'name')
        # }),



        ('Create Contest', {
            #'classes': ('collapse',),
            'fields': (
                'site_sport',
                'name',
                'prize_structure',
                'start',
                #'ends_tonight',
            )
        }),

        ('Advanced Options', {
            'classes': ('collapse',),
            'fields': (
                'ends_tonight',

                'end',
                'max_entries',
                # 'entries',
                'gpp',
                'respawn',
                'doubleup',

                'early_registration',
            )
        }),
    )

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

    def has_delete_permission(self, request, obj=None):
        return False


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

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(contest.models.LiveContest)
class LiveContestAdmin(admin.ModelAdmin):

    list_display = CONTEST_LIST_DISPLAY
    def cancel_and_refund_live_contests(self, request, queryset):
        if queryset.count() > 0:
            for contest in queryset:
                refund_task.delay( contest, force=True )

    actions = [ cancel_and_refund_live_contests ]

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(contest.models.HistoryContest)
class HistoryContestAdmin(admin.ModelAdmin):

    list_display = CONTEST_LIST_DISPLAY

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(contest.models.Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['user','created','updated','contest_link','lineup']
    search_fields = ['user__username']
    list_filter = ['created','updated']

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def contest_link(self, obj):
        """
        Add a button into the admin views so its easy to add a TemplateSchedule to an existing schedule

        :param obj:   the model instance for each row
        :return:
        """

        # the {} in the first argument are like %s for python strings,
        # and the subsequent arguments fill the {}
        return format_html('<a href="{}{}/" class="btn btn-success">{}</a>',
                            "/admin/contest/contest/",
                             obj.pk,
                             str(obj.contest))
