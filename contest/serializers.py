#
# contest/serializers.py

from rest_framework import serializers
from contest.models import Contest

class ContestSerializer(serializers.ModelSerializer):
    # TODO: Create a prize structure serializer to nest data into a contest.
    prize_structure = serializers.StringRelatedField()

    class Meta:

        model = Contest
        fields = ('id','name','sport','status','start',
                  'draft_group','max_entries',
                  'entries','current_entries','gpp',
                  'respawn', 'prize_structure')
