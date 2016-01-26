#
# sports/nba/admin.py

from django.contrib import admin
import sports.admin
import sports.nba.models

@admin.register(sports.nba.models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['srid','name','market','alias']

@admin.register(sports.nba.models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['srid','start','home','away']
    list_filter = ['start','home','away']

@admin.register(sports.nba.models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['srid','position','first_name','last_name']

    list_filter     = sports.admin.PlayerAdmin.list_filter   # + ('',)
    search_fields   = sports.admin.PlayerAdmin.search_fields # + ('more','specific','fields...',)

@admin.register(sports.nba.models.PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = ['game','player','points','three_points_made','rebounds','assists','steals','blocks','turnovers']

@admin.register(sports.nba.models.GameBoxscore)
class GameBoxscoreAdmin(admin.ModelAdmin):
    list_display = ['srid_game','status','title','home_score','home',
                    'away','away_score','quarter','clock','coverage',
                    'home_scoring_json','away_scoring_json']

@admin.register(sports.nba.models.GamePortion)
class GamePortionAdmin(admin.ModelAdmin):
    list_display = ['srid_game','category','sequence']

@admin.register(sports.nba.models.PbpDescription)
class PbpDescriptionAdmin(admin.ModelAdmin):
    list_display = ['pbp','srid_game','category','sequence','idx','description']

@admin.register(sports.nba.models.Injury)
class InjuryAdmin(admin.ModelAdmin):
    list_display = ['iid','srid','comment','status','description']
