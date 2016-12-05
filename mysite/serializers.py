from rest_framework import serializers


class AppConfigSerializer(serializers.Serializer):
    playerImagesBaseUrl = serializers.CharField(max_length=200)
    replayerTimeDelta = serializers.CharField(max_length=200)
    pusher_key = serializers.CharField(max_length=200)
    pusher_channel_prefix = serializers.CharField(max_length=200)
