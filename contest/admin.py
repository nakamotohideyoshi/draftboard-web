#
# contest/admin.py

from django.contrib import admin
import contest.models
import contest.forms
from contest.refund.tasks import refund_task
from .payout.tasks import payout_task
from django.utils.html import format_html

# for ContestPools
CONTEST_POOL_LIST_DISPLAY   = ['site_sport','created','status','prize_structure','start']
CONTEST_POOL_SEARCH_FIELDS  = ['name','status','prize_structure']
CONTEST_POOL_LIST_FILTERS   = ['site_sport','created','status','start']

# for Contests
CONTEST_LIST_DISPLAY    = ['name','created','status','start','end']
CONTEST_SEARCH_FIELDS   = ['name','status']
CONTEST_LIST_FILTERS    = ['name','status','start']

@admin.register(contest.models.LobbyContestPool)
class LobbyContestPoolAdmin(admin.ModelAdmin):

    list_display    = CONTEST_POOL_LIST_DISPLAY
    list_filter     = CONTEST_POOL_LIST_FILTERS
    search_fields   = CONTEST_POOL_SEARCH_FIELDS

    def get_readonly_fields(self, request, obj=None):
        if obj:
            arr = [f.name for f in self.model._meta.fields]
            return arr
        return []

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(contest.models.ContestPool)
class ContestPoolAdmin(admin.ModelAdmin):

    list_display    = CONTEST_POOL_LIST_DISPLAY
    list_filter     = CONTEST_POOL_LIST_FILTERS
    search_fields   = CONTEST_POOL_SEARCH_FIELDS

    def get_readonly_fields(self, request, obj=None):
        if obj:
            arr = [f.name for f in self.model._meta.fields]
            return arr
        return []

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(contest.models.Contest)
class ContestAdmin(admin.ModelAdmin):

    list_display    = CONTEST_LIST_DISPLAY
    list_filters    = CONTEST_LIST_FILTERS
    search_fields   = CONTEST_SEARCH_FIELDS

    def get_readonly_fields(self, request, obj=None):
        if obj:
            arr = [f.name for f in self.model._meta.fields]
            return arr
        return []

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(contest.models.CompletedContest)
class CompletedContestAdmin(admin.ModelAdmin):

    list_display    = CONTEST_LIST_DISPLAY
    list_filters    = CONTEST_LIST_FILTERS
    search_fields   = CONTEST_SEARCH_FIELDS

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

    def contest_link(self, entry):
        if entry.contest is None:
            return '-'

        # otherwise, return a button that can take us to the contest itself
        return format_html('<a href="{}{}/" class="btn btn-success">{}</a>',
                            "/admin/contest/contest/",
                             entry.contest.pk,
                             str(entry.contest))
