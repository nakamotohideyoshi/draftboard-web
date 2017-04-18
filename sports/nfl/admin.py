#
# sports/nfl/admin.py

from django import forms
from django.contrib import admin

import sports.admin
import sports.nfl.models


@admin.register(sports.nfl.models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['srid', 'market', 'name', 'alias']


@admin.register(sports.nfl.models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = sports.admin.GameAdmin.list_display + ['srid', 'status', 'start', 'home', 'away',
                                                          'weather_json']
    list_filter = sports.admin.GameAdmin.list_filter
    search_fields = sports.admin.GameAdmin.search_fields


@admin.register(sports.nfl.models.Player)
class PlayerAdmin(sports.admin.PlayerAdmin):
    list_filter = sports.admin.PlayerAdmin.list_filter  # + ('',)
    search_fields = sports.admin.PlayerAdmin.search_fields  # + ('more','specific','fields...',)


@admin.register(sports.nfl.models.PlayerLineupName)
class PlayerLineupNameAdmin(admin.ModelAdmin):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.list_display_links = (None, )

    lineup_nickname = forms.CharField(widget=forms.Textarea)

    list_display = sports.admin.PlayerLineupName.list_display
    list_filter = sports.admin.PlayerLineupName.list_filter
    search_fields = sports.admin.PlayerLineupName.search_fields
    list_editable = sports.admin.PlayerLineupName.list_editable

    list_per_page = 15

    def has_add_permission(self, request):  # removes Add button
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(sports.nfl.models.PlayerStats)
class PlayerStatsAdmin(sports.admin.PlayerStatsAdmin):
    list_display = [
        'game', 'player', 'fantasy_points',

        # passing stats, receiving, rushing:
        'pass_td', 'pass_yds', 'pass_int',
        'rush_td', 'rush_yds',
        'rec_td', 'rec_yds', 'rec_rec',
        'off_fum_lost', 'off_fum_rec_td',
        'two_pt_conv',

        # dst related:
        'sack', 'ints', 'fum_rec', 'sfty', 'blk_kick',
        'ret_kick_td', 'ret_punt_td', 'ret_int_td',
        'ret_fum_td', 'ret_blk_punt_td', 'ret_fg_td',

        # related to dst points allowed:
        'int_td_against', 'fum_td_against',
        'off_pass_sfty', 'off_rush_sfty', 'off_punt_sfty'
    ]

    search_fields = sports.admin.PlayerStatsAdmin.search_fields  # + ('more','specific','fields...',)
    ordering = sports.admin.PlayerStatsAdmin.ordering  # + ['more']


@admin.register(sports.nfl.models.GameBoxscore)
class GameBoxscoreAdmin(sports.admin.SportGameBoxScoreAdmin):
    list_display = sports.admin.SportGameBoxScoreAdmin.list_display + ['quarter', 'clock', ]


@admin.register(sports.nfl.models.GamePortion)
class GamePortionAdmin(admin.ModelAdmin):
    list_display = ['srid_game', 'category', 'sequence']


@admin.register(sports.nfl.models.PbpDescription)
class PbpDescriptionAdmin(admin.ModelAdmin):
    list_display = ['pbp', 'srid_game', 'category', 'sequence', 'idx', 'description']
