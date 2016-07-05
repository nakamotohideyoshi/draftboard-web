#
# draftgroup/serializers.py

from rest_framework import serializers
from draftgroup.models import (
    DraftGroup,
    Player,
    PlayerUpdate,
    GameUpdate,
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

    class Meta:
        model = PlayerUpdate
        fields = ('category','type','value')

class GameUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameUpdate
        fields = ('category','type','value') # ,'game_id')

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
        model   = DraftGroup
        fields  = ('pk', 'start', 'sport', 'num_games','category')