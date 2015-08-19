#
# draftgroup/serializers.py

from rest_framework import serializers
from draftgroup.models import DraftGroup, Player
import sports.serializers

# PrimaryKeyRelatedField
# PrimaryKeyRelatedField may be used to represent the target of the relationship using its primary key.
#
# For example, the following serializer:
#
# class AlbumSerializer(serializers.ModelSerializer):
#     tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#
#     class Meta:
#         model = Album
#         fields = ('album_name', 'artist', 'tracks')
# Would serialize to a representation like this:
#
# {
#     'album_name': 'The Roots',
#     'artist': 'Undun',
#     'tracks': [
#         89,
#         90,
#         91,
#         ...
#     ]
# }

class PlayerSerializer(serializers.ModelSerializer):

    class Meta:

        model = Player
        #fields = ('id','first_name','last_name','salary','start')
        fields = ('player_id','first_name','last_name','salary','start', 'position','team_alias')

class DraftGroupSerializer(serializers.ModelSerializer):

    players = PlayerSerializer(many=True, read_only=True)

    class Meta:

        model = DraftGroup
        fields = ('pk','start','end','players')


