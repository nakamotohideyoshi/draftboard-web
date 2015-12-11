#
# sports.nhl.serializers.py

from rest_framework import serializers
import sports.serializers
from sports.serializers import InjurySerializer
from .models import Injury, Team

class InjurySerializer(InjurySerializer):

    class Meta:

        model = Injury
        fields = ('iid', 'status','description','srid', 'comment', 'player_id')

class TeamSerializer(sports.serializers.TeamSerializer):

    city = serializers.SerializerMethodField()
    def get_city(self, team):
        return team.market

    class Meta:

        model = Team
        fields = sports.serializers.TeamSerializer.PARENT_FIELDS + ('city',)
        # fields = (
        #     # you shouldnt change id, srid, name, alias
        #     'id', 'srid', 'name', 'alias',
        #
        #     # sport market/city just called city in this serializer
        #     'city'
        # )