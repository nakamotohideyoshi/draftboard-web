from django.contrib import admin

import draftgroup.models


@admin.register(draftgroup.models.DraftGroup)
class DraftGroupAdmin(admin.ModelAdmin):
    list_display = ['created', 'salary_pool', 'start', 'end']


@admin.register(draftgroup.models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['created', 'draft_group', 'player', 'salary']


@admin.register(draftgroup.models.GameTeam)
class GameTeamAdmin(admin.ModelAdmin):
    list_display = ['created', 'draft_group', 'game_srid', 'start', 'alias', 'team_srid']


@admin.register(draftgroup.models.PlayerUpdate)
class PlayerUpdateAdmin(admin.ModelAdmin):
    list_display = ['player', 'sport', 'created', 'category', 'status', 'type', 'value']
    list_filter = ['sport', 'created', 'status', 'category', 'type']
    search_fields = ['update_id', 'player_srid', 'category', 'type', 'value', 'sport']

    @staticmethod
    def player(obj):
        """
        Based on the sport of the PlayerUpdate, we can determine which field that was queried
        in qs.extra to show.
        """
        return "%s %s" % (
            getattr(obj, '%s_first_name' % obj.sport, ''),
            getattr(obj, '%s_last_name' % obj.sport, '')
        )

    def get_queryset(self, request):
        """
        This is a little janky... Because PlayerUpdates have no foreign Key relation to Players,
        we have to fetch names of the players manually, sport by sport because Playres span
        multiple tables and I can't figure out a way to use JOINs and only return one value.
        """
        qs = super(PlayerUpdateAdmin, self).get_queryset(request)

        return qs.extra(select={
            'nfl_first_name': (
                "SELECT first_name FROM nfl_player WHERE player_srid = nfl_player.srid"
            ),
            'nfl_last_name': (
                "SELECT last_name FROM nfl_player WHERE player_srid = nfl_player.srid"
            ),
            # nba
            'nba_first_name': (
                "SELECT first_name FROM nba_player WHERE player_srid = nba_player.srid"
            ),
            'nba_last_name': (
                "SELECT last_name FROM nba_player WHERE player_srid = nba_player.srid"
            ),
            # nhl
            'nhl_first_name': (
                "SELECT first_name FROM nhl_player WHERE player_srid = nhl_player.srid"
            ),
            'nhl_last_name': (
                "SELECT last_name FROM nhl_player WHERE player_srid = nhl_player.srid"
            ),
            # mlb
            'mlb_first_name': (
                "SELECT first_name FROM mlb_player WHERE player_srid = mlb_player.srid"
            ),
            'mlb_last_name': (
                "SELECT last_name FROM mlb_player WHERE player_srid = mlb_player.srid"
            ),
        })


@admin.register(draftgroup.models.GameUpdate)
class GameUpdateAdmin(admin.ModelAdmin):
    list_display = ['created', 'update_id', 'game_srid', 'category', 'type', 'value']
    list_filter = ['created', 'category', 'type', 'game_srid']
    search_fields = ['update_id', 'game_srid', 'category', 'type', 'value']


@admin.register(draftgroup.models.PlayerStatus)
class PlayerStatusAdmin(admin.ModelAdmin):
    list_display = ['player',  'sport', 'status', 'created']
    list_filter = ['sport']

    @staticmethod
    def player(obj):
        """
        Based on the sport of the PlayerUpdate, we can determine which field that was queried
        in qs.extra to show.
        """
        return "%s %s" % (
            getattr(obj, '%s_first_name' % obj.sport, ''),
            getattr(obj, '%s_last_name' % obj.sport, '')
        )

    def get_queryset(self, request):
        """
        This is a little janky... Because PlayerUpdates have no foreign Key relation to Players,
        we have to fetch names of the players manually, sport by sport because Playres span
        multiple tables and I can't figure out a way to use JOINs and only return one value.
        """
        qs = super(PlayerStatusAdmin, self).get_queryset(request)

        return qs.extra(select={
            'nfl_first_name': (
                "SELECT first_name FROM nfl_player WHERE player_srid = nfl_player.srid"
            ),
            'nfl_last_name': (
                "SELECT last_name FROM nfl_player WHERE player_srid = nfl_player.srid"
            ),
            # nba
            'nba_first_name': (
                "SELECT first_name FROM nba_player WHERE player_srid = nba_player.srid"
            ),
            'nba_last_name': (
                "SELECT last_name FROM nba_player WHERE player_srid = nba_player.srid"
            ),
            # nhl
            'nhl_first_name': (
                "SELECT first_name FROM nhl_player WHERE player_srid = nhl_player.srid"
            ),
            'nhl_last_name': (
                "SELECT last_name FROM nhl_player WHERE player_srid = nhl_player.srid"
            ),
            # mlb
            'mlb_first_name': (
                "SELECT first_name FROM mlb_player WHERE player_srid = mlb_player.srid"
            ),
            'mlb_last_name': (
                "SELECT last_name FROM mlb_player WHERE player_srid = mlb_player.srid"
            ),
        })
