from __future__ import absolute_import

#
# replayer/tasks.py
from django.utils import timezone
from util.loaddata import LoadData
from mysite.celery_app import app
from replayer.classes import ReplayManager
from celery.contrib.abortable import AbortableTask
from replayer.models import TimeMachine
from django.core import management

@app.task(bind=True)
def reset_db_for_replay(self):
    """
    Wipes out db using
        >>> from django.core import management
        >>> management.call_command('flush', verbosity=0, interactive=False)
            ... and it can be reloaded by something like ...
        >>> management.call_command('loaddata', 'test_data', verbosity=0)

    :return:
    """
    print('calling >>> management.call_command("flush", verbosity=1, interactive=False)')
    #management.call_command('flush', verbosity=1, interactive=False)
    management.call_command('flush', verbosity=1, interactive=False)
    print('done with flush command')

@app.task(bind=True)
def snapshot_db_for_replay(self):
    """
    Wipes out db using
        >>> from django.core import management
        >>> management.call_command('dumpdata', '--output', 'dumped.json' verbosity=0)

    :return:
    """
    print('calling >>> management.call_command("dumpdata", verbosity=1, interactive=False)')
    from django.conf import settings
    filename = settings.SMUGGLER_FIXTURE_DIR + '/live_db_dump.json'
    management.call_command('dumpdata', '--output', filename, verbosity=1, interactive=False)
    print('done with dumpdata command')

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



