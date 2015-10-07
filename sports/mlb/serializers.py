#
# sports.mlb.serializers.py

from sports.serializers import InjurySerializer
from .models import Injury

class InjurySerializer(InjurySerializer):

    class Meta:

        model = Injury
        fields = ('iid', 'status','description','srid', 'comment', 'player_id')