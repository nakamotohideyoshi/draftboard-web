#
# sports/mlb/admin.py

from django.contrib import admin
import sports.mlb.models
import sports.admin
from django import forms

@admin.register(sports.mlb.models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['srid','market','name']

@admin.register(sports.mlb.models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display    = ['srid','status','start','home','away','day_night','game_number']
    list_filter     = sports.admin.GameAdmin.list_filter
    search_fields   = sports.admin.GameAdmin.search_fields

@admin.register(sports.mlb.models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['preferred_name'] + sports.admin.PlayerAdmin.list_display

    list_filter     = sports.admin.PlayerAdmin.list_filter   # + ('',)
    search_fields   = sports.admin.PlayerAdmin.search_fields # + ('more','specific','fields...',)

@admin.register(sports.mlb.models.PlayerLineupName)
class PlayerLineupNameAdmin(admin.ModelAdmin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_display_links = (None, )

    lineup_nickname = forms.CharField( widget=forms.Textarea )

    list_display    = sports.admin.PlayerLineupName.list_display
    list_filter     = sports.admin.PlayerLineupName.list_filter
    search_fields   = sports.admin.PlayerLineupName.search_fields
    list_editable   = sports.admin.PlayerLineupName.list_editable

    list_per_page   = 15

    def has_add_permission(self, request): # removes Add button
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(sports.mlb.models.PlayerStatsHitter)
class PlayerStatsHitterAdmin(sports.admin.PlayerStatsAdmin):
    list_display = ['game','player','fantasy_points','bb','s','d','t','hr','rbi','r','hbp','sb','cs','ktotal','ab','ap','lob','xbh']
    search_fields   = sports.admin.PlayerStatsAdmin.search_fields # + ('more','specific','fields...',)
    ordering        = sports.admin.PlayerStatsAdmin.ordering # + ['more']

@admin.register(sports.mlb.models.PlayerStatsPitcher)
class PlayerStatsPitcherAdmin(sports.admin.PlayerStatsAdmin):
    list_display = ['game','player','fantasy_points','ip_1','ip_2','win','loss','qstart','ktotal','er','h','bb','hbp','cg','cgso','nono']
    search_fields   = sports.admin.PlayerStatsAdmin.search_fields # + ('more','specific','fields...',)
    ordering        = sports.admin.PlayerStatsAdmin.ordering

@admin.register(sports.mlb.models.GameBoxscore)
class GameBoxscoreAdmin(admin.ModelAdmin):
    list_display = ['srid_game','status','title','home_score','home',
                    'away','away_score','inning','inning_half','coverage',
                    'home_scoring_json','away_scoring_json',
                    'srid_home_pp', 'srid_away_pp']

@admin.register(sports.mlb.models.GamePortion)
class GamePortionAdmin(admin.ModelAdmin):
    list_display = ['srid_game','category','sequence']

@admin.register(sports.mlb.models.PbpDescription)
class PbpDescriptionAdmin(admin.ModelAdmin):
    list_display = ['pbp','srid_game','category','sequence','idx','description']

@admin.register(sports.mlb.models.Injury)
class InjuryAdmin(admin.ModelAdmin):
    list_display = ['iid','status','description']