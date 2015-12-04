#
# lobby/serializers.py

from rest_framework import serializers
from lobby.models import ContestBanner

class ContestBannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContestBanner
        fields = ('start_time','end_time','image_url','links_to')
