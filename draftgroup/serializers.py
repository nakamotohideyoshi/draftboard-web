#
# draftgroup/serializers.py

from rest_framework import serializers
from draftgroup.models import DraftGroup, Player
from roster.models import RosterSpot

class PlayerSerializer(serializers.ModelSerializer):

    game_srid = serializers.SerializerMethodField()
    def get_game_srid(self, draft_group_player):
        return draft_group_player.game_team.game_srid

    team_srid = serializers.SerializerMethodField()
    def get_team_srid(self, draft_group_player):
        return draft_group_player.game_team.team_srid

    class Meta:
        model = Player
        fields = ('player_id', 'name', 'salary',
                  'start', 'position', 'fppg',
                  'team_alias', 'game_srid', 'team_srid')

class AbstractDraftGroupSerializer(serializers.ModelSerializer):
    """
    super class which has the sport for the DraftGroup
    """

    sport = serializers.SerializerMethodField()

    def get_sport(self, draft_group):
        return draft_group.salary_pool.site_sport.name

class DraftGroupSerializer(AbstractDraftGroupSerializer):

    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = DraftGroup
        fields = ('pk', 'start', 'end', 'sport', 'players')

class UpcomingDraftGroupSerializer(AbstractDraftGroupSerializer):

    class Meta:
        model   = DraftGroup
        fields  = ('pk', 'start', 'sport', 'num_games','category')