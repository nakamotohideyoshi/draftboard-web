#
# sports/mlb/admin.py

from django.contrib import admin
import sports.mlb.models

@admin.register(sports.mlb.models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['srid','market','name']

@admin.register(sports.mlb.models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['srid','start','home','away','day_night','game_number']
    list_filter = ['start','home','away']

@admin.register(sports.mlb.models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['srid','position','preferred_name','first_name','last_name']

@admin.register(sports.mlb.models.PlayerStatsHitter)
class PlayerStatsHitterAdmin(admin.ModelAdmin):
    list_display = ['game','player','bb','s','d','t','hr','rbi','r','hbp','sb','cs','ktotal','ab','ap','lob','xbh']

@admin.register(sports.mlb.models.PlayerStatsPitcher)
class PlayerStatsPitcherAdmin(admin.ModelAdmin):
    list_display = ['game','player','ip_1','ip_2','win','loss','qstart','ktotal','er','h','bb','hbp','cg','cgso','nono']

@admin.register(sports.mlb.models.GameBoxscore)
class GameBoxscoreAdmin(admin.ModelAdmin):
    list_display = ['srid_game','status','title','home_score','home',
                    'away','away_score','inning','inning_half','coverage',
                    'home_scoring_json','away_scoring_json']

@admin.register(sports.mlb.models.GamePortion)
class GamePortionAdmin(admin.ModelAdmin):
    list_display = ['srid_game','category','sequence']

@admin.register(sports.mlb.models.PbpDescription)
class PbpDescriptionAdmin(admin.ModelAdmin):
    list_display = ['pbp','srid_game','category','sequence','idx','description']

@admin.register(sports.mlb.models.Injury)
class InjuryAdmin(admin.ModelAdmin):
    list_display = ['iid','status','description']