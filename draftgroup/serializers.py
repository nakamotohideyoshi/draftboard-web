#
# draftgroup/serializers.py

from rest_framework import serializers
from draftgroup.models import DraftGroup, Player
from roster.models import RosterSpot


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('player_id', 'name', 'salary', 'start', 'position',
                  'team_alias')


class DraftGroupSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    sport = serializers.SerializerMethodField()

    def get_sport(self, draft_group):
        return draft_group.salary_pool.site_sport.name

    class Meta:
        model = DraftGroup
        fields = fields = ('pk', 'start', 'end', 'sport', 'players')
