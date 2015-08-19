#
# draftgroup/admin.py

from django.contrib import admin
import draftgroup.models

@admin.register(draftgroup.models.DraftGroup)
class DraftGroupAdmin(admin.ModelAdmin):
    list_display = ['created','salary_pool','start','end']

@admin.register(draftgroup.models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['created','draft_group','player','salary']


@admin.register(draftgroup.models.GameTeam)
class GameTeamAdmin(admin.ModelAdmin):
    list_display = ['created','draft_group','game_srid','start','alias','team_srid']