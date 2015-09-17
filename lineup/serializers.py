#
# lineup/serializers.py

from rest_framework import serializers
from lineup.models import Lineup, Player
from sports.nfl.models import Player as NflPlayer
from sports.nba.models import Player as NbaPlayer
from sports.nfl.models import Team as NflTeam
from sports.nba.models import Team as NbaTeam
from sports.models import Position, Injury

import draftgroup.models


class NflTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = NflTeam
        fields = ('id', 'alias', 'market', 'name')


class NbaTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = NbaTeam
        fields = ('id', 'alias', 'market', 'name')


class InjurySerializer(serializers.ModelSerializer):
    class Meta:
        model = Injury


# Choose the correct serializer for the sport the player plays.
class GenericSportPlayerSerializer(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, NflPlayer):
            serializer = NflPlayerSerializer(value)
        elif isinstance(value, NbaPlayer):
            serializer = NbaPlayerSerializer(value)
        else:
            raise Exception('Unexpected type of player object in GenericSportPlayerSerializer')

        return serializer.data


class NflPlayerSerializer(serializers.ModelSerializer):
    injury = InjurySerializer()
    team = NflTeamSerializer()

    class Meta:
        model = NflPlayer
        fields = ('first_name', 'last_name', 'injury', 'status', 'team')


class NbaPlayerSerializer(serializers.ModelSerializer):
    injury = InjurySerializer()
    team = NbaTeamSerializer()

    class Meta:
        model = NbaPlayer
        fields = ('first_name', 'last_name', 'injury', 'status', 'team')


class PlayerSerializer(serializers.ModelSerializer):
    player_meta = GenericSportPlayerSerializer(read_only=True, source='player')
    roster_spot = serializers.StringRelatedField()

    class Meta:
        model = Player
        fields = ('player_id', 'full_name', 'roster_spot', 'idx', 'player_meta')


class LineupSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Lineup
        fields = ('id', 'user', 'sport', 'fantasy_points', 'draft_group', 'players')


class CreateLineupSerializer(serializers.Serializer):

    draft_group = serializers.IntegerField()

    players = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=9999999)
    )

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        draft_group_id = data['draft_group']
        if draft_group_id is None:
            raise serializers.ValidationError("invalid draft_group id")
        try:
            draftgroup.models.DraftGroup.objects.get(pk=draft_group_id)
        except draftgroup.models.DraftGroup.DoesNotExist:
            raise serializers.ValidationError('invalid draft_group id')

        return data


class EditLineupSerializer(serializers.Serializer):

    lineup = serializers.IntegerField()

    players = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=9999999)
    )
