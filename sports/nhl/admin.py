#
# sports/nhl/admin.py

from django.contrib import admin
import sports.nba.models

@admin.register(sports.nhl.models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['srid','name']

@admin.register(sports.nhl.models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['srid','start','home','away']

@admin.register(sports.nhl.models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['srid','first_name','last_name']

@admin.register(sports.nhl.models.PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = [
        # skater stats:
        'game','player','position','primary_position','fantasy_points','goal','assist','sog','blk','sh_goal','pp_goal', 'so_goal',
        # goalie stats:
        'w', 'l', 'otl', 'saves', 'ga', 'shutout'
    ]

@admin.register(sports.nhl.models.GameBoxscore)
class GameBoxscoreAdmin(admin.ModelAdmin):
    list_display = ['srid_game','status','title','home_score','home',
                    'away','away_score','period','clock','coverage',
                    'home_scoring_json','away_scoring_json']

@admin.register(sports.nhl.models.GamePortion)
class GamePortionAdmin(admin.ModelAdmin):
    list_display = ['srid_game','category','sequence']

@admin.register(sports.nhl.models.PbpDescription)
class PbpDescriptionAdmin(admin.ModelAdmin):
    list_display = ['pbp','srid_game','category','sequence','idx','description']

@admin.register(sports.nhl.models.Injury)
class InjuryAdmin(admin.ModelAdmin):
    list_display = ['iid','srid','comment','status','description']