#
# lineup/serializers.py

from rest_framework import serializers
from lineup.models import Lineup, Player
import draftgroup.models


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('player_id', 'full_name', 'lineup', 'roster_spot', 'idx')


class LineupSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Lineup
        fields = ('id', 'user', 'fantasy_points', 'draft_group', 'players')


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
