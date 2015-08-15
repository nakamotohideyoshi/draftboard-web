#
# draftgroup/serializers.py

from rest_framework import serializers
from draftgroup.models import DraftGroup, Player

class DraftGroupSerializer(serializers.ModelSerializer):

    class Meta:

        model = DraftGroup
        fields = ('pk','start','end')

# class PlayerSerializer(serializers.ModelSerializer):
#
#     class Meta:
#
#         model = Player
#         fields = ('player','salary','start','draft_group')
