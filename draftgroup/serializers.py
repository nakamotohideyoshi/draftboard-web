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
    def get_game_srid(self, draft_group_player):
        return draft_group_player.game_team.game_srid

    team_srid = serializers.SerializerMethodField()
    def get_team_srid(self, draft_group_player):
        return draft_group_player.game_team.team_srid

    player_srid = serializers.SerializerMethodField()
    def get_player_srid(self, draft_group_player):
        return draft_group_player.player.srid

    class Meta:
        model = Player
        fields = ('player_id', 'name', 'salary',
                  'start', 'position', 'fppg',
                  'team_alias', 'game_srid', 'team_srid', 'player_srid')


class PlayerUpdateSerializer(serializers.ModelSerializer):

    srid = serializers.SerializerMethodField()
    def get_srid(self, obj):
        return obj.player_srid

    class Meta:
        model = PlayerUpdate
        fields = ('updated_at','category','type','value','srid','status','source_origin','url_origin')


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
        fields = ('updated_at','category','type','value','srid','status','source_origin','url_origin')


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
        fields = ('pk', 'start', 'sport', 'num_games','category')


