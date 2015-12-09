from __future__ import absolute_import

#
# replayer/tasks.py
from os.path import join
from django.utils import timezone
from util.loaddata import LoadData
from mysite.celery_app import app
from replayer.classes import ReplayManager
from celery.contrib.abortable import AbortableTask
from replayer.models import TimeMachine
from django.core import management
from django.conf import settings
import subprocess

from django.core.management.color import no_style
#from django.core.management.commands.dumpdata import Command as DumpData
# from django.core.management.commands.loaddata import Command as LoadData
from django.db.utils import DEFAULT_DB_ALIAS
from django.http import HttpResponse
from django.utils.six import StringIO
from smuggler import settings as smugger_settings

@app.task(bind=True)
def reset_db_for_replay(self, s3file):
    """
    ssh into the remote aws replay helper server,
    and use heroku to restore a database dump

    :return:
    """

    #
    # rp.sub_call('ssh -i coderden.pem ubuntu@ec2-52-11-96-189.us-west-2.compute.amazonaws.com "heroku pg:info --app rio-dfs"')
    cmd = 'ssh -i coderden.pem ubuntu@ec2-52-11-96-189.us-west-2.compute.amazonaws.com "fab restore_db --set s3file=%s"' % s3file
    print( cmd )
    subprocess.call( cmd )

@app.task(bind=True)
def snapshot_db_for_replay(self):
    """
    saves a snapshot of the current database with internal use of manage.py dumpdata
    :return:
    """
    print('save snapshot default')
    save_snapshot_simple()
    print('saved snapshot default')

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

def save_snapshot_simple():
    stream = serialize_to_response()
    save_stream_to_file(stream)  # saves with default name

def save_stream_to_file(stream, filename='replayer_snapshot.json'):
    fullpath = join( settings.SMUGGLER_FIXTURE_DIR, filename)
    with open(fullpath, 'wb') as fd:
        fd.write( stream.getvalue().encode('utf-8') )

def serialize_to_response(app_labels=None, exclude=None, response=None,
                          format=smugger_settings.SMUGGLER_FORMAT,
                          indent=smugger_settings.SMUGGLER_INDENT):
    app_labels = app_labels or []
    exclude = exclude or []
    stream = StringIO()
    error_stream = StringIO()
    dumpdata = DumpData()
    dumpdata.style = no_style()
    dumpdata.execute(*app_labels, **{
        'stdout': stream,
        'stderr': error_stream,
        'exclude': exclude,
        'format': format,
        'indent': indent,
        'use_natural_foreign_keys': True,
        'use_natural_primary_keys': True
    })
    # response.write(stream.getvalue())
    # return response
    return stream