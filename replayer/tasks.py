from __future__ import absolute_import

#
# replayer/tasks.py
from django.utils import timezone
from util.loaddata import LoadData
from mysite.celery_app import app
from replayer.classes import ReplayManager

@app.task
def load_replay( timemachine ):
    """

    :param timemachine: replayer.models.TimeMachine object
    :return:
    """

    filename = timemachine.replay

    loader = LoadData(filename)  # validates filename
    loader.load()

    rp = ReplayManager(timemachine=timemachine)

    # load_db=False runs whats already in the replayer.models.Update table
    rp.play(load_db=False)

