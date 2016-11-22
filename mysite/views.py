from rest_framework import generics
from rest_framework.response import Response
from .serializers import AppConfigSerializer
from django.conf import settings
from .context_processors import delta_now_prefix


class AppConfigView(generics.GenericAPIView):
    """
    Expose general app configuration info that is intended for clients to use.
    """
    serializer_class = AppConfigSerializer

    @staticmethod
    def get(request):
        serialized_data = {
            'replayerTimeDelta': delta_now_prefix(request),
            'pusherKey': settings.PUSHER_KEY,
            'pusherChannelPrefix': settings.PUSHER_CHANNEL_PREFIX,
            'playerImagesBaseUrl': settings.PLAYER_IMAGES_URL,
        }
        return Response(serialized_data)

