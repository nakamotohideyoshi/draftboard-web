#
# sports/nba/admin.py

from django.contrib import admin
import sports.admin
import sports.nba.models
from django import forms

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

@admin.register(sports.nba.models.PlayerLineupName)
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

@admin.register(sports.nba.models.PlayerStats)
class PlayerStatsAdmin(sports.admin.PlayerStatsAdmin):
    list_display = ['game','player','points','three_points_made','rebounds','assists','steals','blocks','turnovers']

    # list_filter     = sports.admin.PlayerStatsAdmin.list_filter   # + ('',)
    search_fields   = sports.admin.PlayerStatsAdmin.search_fields # + ('more','specific','fields...',)

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
