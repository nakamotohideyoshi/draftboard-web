#
# contest/admin.py

from django.contrib import admin
import contest.models
import contest.forms

CONTEST_LIST_DISPLAY = ['created','status','name','start','end']

@admin.register(contest.models.Contest)
class ContestAdmin(admin.ModelAdmin):
    #list_display = CONTEST_LIST_DISPLAY
    form = contest.forms.ContestForm

    # create some "sections" of the form"
    fieldsets = (
        (None, {
            'fields': ('clone_from', 'name')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (
                'prize_structure',
                'start',
                'end'
            )
        }),
    )


@admin.register(contest.models.UpcomingContest)
class UpcomingContestAdmin(admin.ModelAdmin):
    list_display = CONTEST_LIST_DISPLAY

@admin.register(contest.models.LiveContest)
class LiveContestAdmin(admin.ModelAdmin):
    list_display = CONTEST_LIST_DISPLAY

@admin.register(contest.models.HistoryContest)
class HistoryContestAdmin(admin.ModelAdmin):
    list_display = CONTEST_LIST_DISPLAY

@admin.register(contest.models.Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['created','updated','contest','lineup']