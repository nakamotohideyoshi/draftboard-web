#
# contest/serializers.py

from rest_framework import serializers
from contest.models import Contest

class ContestSerializer(serializers.ModelSerializer):

    class Meta:

        model = Contest
        fields = ('name','status','start')