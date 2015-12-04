from __future__ import absolute_import

#
# replayer/tasks.py
from django.utils import timezone
from util.loaddata import LoadData
from mysite.celery_app import app
from replayer.classes import ReplayManager
from celery.contrib.abortable import AbortableTask
from replayer.models import TimeMachine

@app.task(bind=True, base=AbortableTask)
def load_replay(self, timemachine):
    """
    Loads the data for the TimeMachine objects
    replay into the Update table and then plays
    it back thru the system to  simulate real
    stats that already happened.

    To abort this task while its running you may do this:

        >>> result = load_replay.AsyncResult( THE_TASK_ID )
        >>> result.abort()

    :param timemachine: replayer.models.TimeMachine object
    :return:
    """

    filename = timemachine.replay

    loader = LoadData(filename)  # validates filename
    loader.load()

    rp = ReplayManager(timemachine=timemachine)

    # load_db=False runs whats already in the replayer.models.Update table
    mode = timemachine.playback_mode
    if mode == TimeMachine.PLAYBACK_MODE_PLAY_ALL:

        rp.play(load_db=False)

    elif mode == TimeMachine.PLAYBACK_MODE_PLAY_TO_TARGET:

        rp.play(load_db=False, play_until=timemachine.target)



