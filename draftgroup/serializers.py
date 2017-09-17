#
# draftgroup/serializers.py

from rest_framework import serializers
from draftgroup.models import (
    DraftGroup,
    Player,
    PlayerUpdate,
    GameUpdate,
    PlayerStatus,
)
from roster.models import RosterSpot


class PlayerSerializer(serializers.ModelSerializer):
    game_srid = serializers.SerializerMethodField()
    player_srid = serializers.SerializerMethodField()
    team_srid = serializers.SerializerMethodField()
    season_fppg = serializers.SerializerMethodField()

    @staticmethod
    def get_game_srid(draft_group_player):
        return draft_group_player.game_team.game_srid

    @staticmethod
    def get_team_srid(draft_group_player):
        return draft_group_player.game_team.team_srid

    @staticmethod
    def get_player_srid(draft_group_player):
        return draft_group_player.player.srid

    @staticmethod
    def get_season_fppg(draft_group_player):
        return draft_group_player.player.season_fppg

    class Meta:
        model = Player
        fields = ('player_id', 'name', 'salary',
                  'start', 'position', 'fppg',
                  'team_alias', 'game_srid', 'team_srid', 'player_srid', 'season_fppg')


class PlayerUpdateSerializer(serializers.ModelSerializer):
    srid = serializers.SerializerMethodField()

    def get_srid(self, obj):
        return obj.player_srid

    class Meta:
        model = PlayerUpdate
        fields = ('updated_at', 'category', 'type', 'value', 'srid', 'status', 'source_origin', 'url_origin',
                  'notes', 'analysis', 'headline')


class PlayerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStatus
        fields = ('player_srid', 'status')


class GameUpdateSerializer(serializers.ModelSerializer):
    srid = serializers.SerializerMethodField()

    def get_srid(self, obj):
        return obj.game_srid

    class Meta:
        model = GameUpdate
        fields = ('updated_at', 'category', 'type', 'value', 'srid', 'status', 'source_origin', 'url_origin')


class AbstractDraftGroupSerializer(serializers.ModelSerializer):
    """
    super class which has the sport for the DraftGroup
    """

    sport = serializers.SerializerMethodField()

    def get_sport(self, draft_group):
        return draft_group.salary_pool.site_sport.name


class DraftGroupSerializer(AbstractDraftGroupSerializer):
    players = PlayerSerializer(many=True, read_only=True)

    game_updates = GameUpdateSerializer(source='gameupdate_set', many=True, read_only=True)

    class Meta:
        model = DraftGroup
        fields = ('pk', 'start', 'end', 'sport', 'game_updates', 'players', 'closed')


class UpcomingDraftGroupSerializer(AbstractDraftGroupSerializer):
    class Meta:
        model = DraftGroup
        fields = ('pk', 'start', 'sport', 'num_games', 'category')
