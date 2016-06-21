#
# sports/nhl/admin.py

from django.contrib import admin
import sports.nba.models
import sports.admin
from django import forms

@admin.register(sports.nhl.models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['srid','name']

@admin.register(sports.nhl.models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display    = ['srid','status','start','home','away']
    list_filter     = sports.admin.GameAdmin.list_filter
    search_fields   = sports.admin.GameAdmin.search_fields

@admin.register(sports.nhl.models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = sports.admin.PlayerAdmin.list_display

    list_filter     = sports.admin.PlayerAdmin.list_filter   # + ('',)
    search_fields   = sports.admin.PlayerAdmin.search_fields # + ('more','specific','fields...',)

@admin.register(sports.nhl.models.PlayerLineupName)
class PlayerLineupNameAdmin(admin.ModelAdmin):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.list_display_links = (None, )

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

@admin.register(sports.nhl.models.PlayerStats)
class PlayerStatsAdmin(sports.admin.PlayerStatsAdmin):
    list_display = [
        # skater stats:
        'game','player','fantasy_points', 'position','goal','assist','sog','blk','sh_goal','pp_goal', 'so_goal',
        # goalie stats:
        'w', 'l', 'otl', 'saves', 'ga', 'shutout'
    ]
    search_fields   = sports.admin.PlayerStatsAdmin.search_fields # + ('more','specific','fields...',)
    ordering        = sports.admin.PlayerStatsAdmin.ordering # + ['more']

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