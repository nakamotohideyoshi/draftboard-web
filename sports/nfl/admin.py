#
# sports/nfl/admin.py

from django.contrib import admin
import sports.nfl.models

@admin.register(sports.nfl.models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['srid','name']

@admin.register(sports.nfl.models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['srid','start','home','away']

@admin.register(sports.nfl.models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['srid','first_name','last_name']

@admin.register(sports.nfl.models.PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = ['game','player']

# @admin.register(sports.nfl.models.GameBoxscore)
# class GameBoxscoreAdmin(admin.ModelAdmin):
#     list_display = ['srid_game','status','title','home_score','home',
#                     'away','away_score','quarter','clock','coverage',
#                     'home_scoring_json','away_scoring_json']
