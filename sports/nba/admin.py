#
# sports/nba/admin.py

from django.contrib import admin
import sports.nba.models

@admin.register(sports.nba.models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['srid','name']

@admin.register(sports.nba.models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['srid','start','home','away']

@admin.register(sports.nba.models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['srid','first_name','last_name']

@admin.register(sports.nba.models.PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = ['game','player','points']
