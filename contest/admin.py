#
# contest/admin.py

from django.contrib import admin
import contest.models

@admin.register(contest.models.Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ['created','name','start','today_only','end']