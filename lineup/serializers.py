#
# lineup/serializers.py

from rest_framework import serializers
from lineup.models import Lineup

class LineupSerializer(serializers.ModelSerializer):

    class Meta:

        model   = Lineup
        fields  = ('name',)
