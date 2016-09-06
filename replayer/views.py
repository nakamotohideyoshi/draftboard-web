#
# view.py

from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from replayer.tasks import (
    reset_replay_test,
)
from replayer.classes import (
    ReplayManager,
)

class PauseActiveReplayAPIView(APIView):

    def post(self, request, *args, **kwags):
        replay_manager = ReplayManager()
        replay_manager.flag_paused(True)
        return Response(status=200)

class ResumeActiveReplayAPIView(APIView):

    def post(self, request, *args, **kwargs):
        replay_manager = ReplayManager()
        replay_manager.flag_paused(False)
        return Response(status=200)

class ResetReplayAPIView(APIView):

    def post(self, request, *args, **kwargs):

        reset_replay_test.delay('s3file_TODO')

        return Response(status=200)