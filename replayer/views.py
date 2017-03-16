from rest_framework.response import Response
from rest_framework.views import APIView

from replayer.classes import (
    ReplayManager,
)
from replayer.tasks import (
    reset_replay_test,
)


class PauseActiveReplayAPIView(APIView):
    """
    note: pause will override any fast-forward / playback speed values actively set.
    """

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


class FastForwardAPIView(APIView):
    """
    set the playback speed, ie: fast forward.
    any integer from 1 to 100 (normal, to fastest) can be set.
    values outside less than 1, or greater than 100 are set to 1 or 100 respectively.

         example:

           /replayer/fast-forward/1/       -> 1x speed (default)
           /replayer/fast-forward/2/       -> 2x speed
           /replayer/fast-forward/10/      -> 57x speed

    """

    def post(self, request, speed, *args, **kwargs):
        # note the speed value passed in may be adjusted later on if its out of range.
        # print('speed:', str(speed))
        if isinstance(speed, str):
            speed = int(speed)

        # set the cache value that tells the replayer to fast forward
        replay_manager = ReplayManager()
        replay_manager.fast_forward(speed)

        #
        return Response(status=200)
