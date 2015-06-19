#
# sports/nfl/admin.py

from django.contrib import admin
import sports.nfl.models

@admin.register(sports.nfl.models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['srid','market','name','alias']

@admin.register(sports.nfl.models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['srid','status','start','home','away','weather_json']
    list_filter = ['start','home','away']

@admin.register(sports.nfl.models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['srid','position','first_name','last_name']

@admin.register(sports.nfl.models.PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = [
        'game','player',

        # passing stats, receiving, rushing:
        'pass_td','pass_yds','pass_int',
        'rush_td','rush_yds',
        'rec_td','rec_yds','rec_rec',
        'off_fum_lost','off_fum_rec_td',
        'two_pt_conv',

        # dst related:
        'sack','ints','fum_rec','sfty','blk_kick',
        'ret_kick_td','ret_punt_td','ret_int_td',
        'ret_fum_td','ret_blk_punt_td','ret_fg_td',

        # related to dst points allowed:
        'int_td_against','fum_td_against',
        'off_pass_sfty','off_rush_sfty','off_punt_sfty'
    ]

@admin.register(sports.nfl.models.GameBoxscore)
class GameBoxscoreAdmin(admin.ModelAdmin):
    list_display = ['srid_game','status','title','home_score','home',
                    'away','away_score','quarter','clock','coverage',
                    'home_scoring_json','away_scoring_json']

@admin.register(sports.nfl.models.GamePortion)
class GamePortionAdmin(admin.ModelAdmin):
    list_display = ['srid_game','category','sequence']

@admin.register(sports.nfl.models.PbpDescription)
class PbpDescriptionAdmin(admin.ModelAdmin):
    list_display = ['pbp','srid_game','category','sequence','idx','description']

@admin.register(sports.nfl.models.Injury)
class InjuryAdmin(admin.ModelAdmin):
    list_display = ['iid','srid','practice_status','status','description']