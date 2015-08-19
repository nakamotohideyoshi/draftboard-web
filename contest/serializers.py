#
# contest/serializers.py

from rest_framework import serializers
from contest.models import Contest

class ContestSerializer(serializers.ModelSerializer):

    class Meta:

        model = Contest
        fields = ('name','sport','status','start',
                  'draft_group','max_entries',
                  'entries','current_entries','gpp',
                  'respawn')