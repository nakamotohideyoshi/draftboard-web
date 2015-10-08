#
# lineup/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers
from lineup.models import Lineup, Player
from sports.nfl.models import Player as NflPlayer
from sports.nfl.models import Injury as NflInjury
from sports.nba.models import Player as NbaPlayer
from sports.nba.models import Injury as NbaInjury
from sports.nfl.models import Team as NflTeam
from sports.nba.models import Team as NbaTeam

import draftgroup.models


# NFL specific
class NflTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = NflTeam
        fields = ('id', 'alias', 'market', 'name')


class NflInjurySerializer(serializers.ModelSerializer):
    class Meta:
        model = NflInjury


class NflPlayerSerializer(serializers.ModelSerializer):
    injury = NflInjurySerializer()
    team = NflTeamSerializer()

    class Meta:
        model = NflPlayer
        fields = ('first_name', 'last_name', 'injury', 'status', 'team')


# NBA specific
class NbaTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = NbaTeam
        fields = ('id', 'alias', 'market', 'name')


class NbaInjurySerializer(serializers.ModelSerializer):
    class Meta:
        model = NbaInjury


class NbaPlayerSerializer(serializers.ModelSerializer):
    injury = NbaInjurySerializer()
    team = NbaTeamSerializer()

    class Meta:
        model = NbaPlayer
        fields = ('first_name', 'last_name', 'injury', 'status', 'team')


class LineupUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class LineupIdSerializer(serializers.ModelSerializer):
    user = LineupUsernameSerializer()

    class Meta:
        model = Lineup
        fields = ('id', 'user')


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
        fields = ('id', 'user', 'name', 'sport', 'fantasy_points', 'draft_group', 'players')


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
