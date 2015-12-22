from __future__ import absolute_import

#
# replayer/tasks.py
from django.core.cache import cache
from os.path import join
from django.utils import timezone
from mysite.celery_app import app
# from replayer.classes import ReplayManager
import replayer.classes
from celery.contrib.abortable import AbortableTask
from replayer.models import TimeMachine
from django.core import management
from django.conf import settings
import subprocess

from django.core.management.color import no_style
from django.core.management.commands.dumpdata import Command as DumpData
# from django.core.management.commands.loaddata import Command as LoadData
from django.db.utils import DEFAULT_DB_ALIAS
from django.http import HttpResponse
from django.utils.six import StringIO
from smuggler import settings as smugger_settings


LOCK_EXPIRE = 60

@app.task(bind=True)
def reset_db_for_replay(self, s3file):
    """
    ssh into the remote aws replay helper server,
    and use heroku to restore a database dump

    :return:
    """

    lock_id = 'task-LOCK-%s' % 'reset_db_for_replay'
    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:

            #
            # locked code runs in here

            #
            # rp.sub_call('ssh -i coderden.pem ubuntu@ec2-52-11-96-189.us-west-2.compute.amazonaws.com "heroku pg:info --app draftboard-staging"')
            cmd = 'ssh -o "StrictHostKeyChecking no" -i coderden.pem ubuntu@ec2-52-11-96-189.us-west-2.compute.amazonaws.com "fab restore_db --set s3file=%s"' % s3file
            print( cmd )
            rp = replayer.classes.ReplayManager()
            # subprocess.call( cmd )
            rp.sub_call( cmd )

        finally:
            release_lock()

@app.task(bind=True)
def fill_contests(self, timemachine):
    """
    Fills all registering contests it can find with random users.

    :param timemachine:
    :return:
    """

    lock_id = 'task-LOCK-%s' % 'fill_contests'
    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)

    # make sure only 1 task can run this code at a time!
    if acquire_lock():
        try:

            #
            # store this tasks id in the timemachine for future use
            timemachine.fill_contests_task_id = self.request.id
            timemachine.save()

            timemachine.fill_contest_status = 'WORKING...'
            timemachine.save()

            rp = replayer.classes.ReplayManager()
            rp.fill_contests()

            timemachine.fill_contest_status = 'DONE'
            timemachine.save()

        finally:
            release_lock()

@app.task(bind=True, base=AbortableTask)
def play_replay(self, timemachine):
    """
    Play the Update objects for the timemachine specified

    To abort this task while its running you may do this:

        >>> result = play_replay.AsyncResult( THE_TASK_ID )
        >>> result.abort()

    :param timemachine: replayer.models.TimeMachine object
    :return:
    """

    lock_id = 'task-LOCK-%s' % 'play_replay'
    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)

    # make sure only 1 task can run this code at a time
    if acquire_lock():
        try:
            #
            # store this tasks id in the timemachine for future use
            timemachine.playback_task_id = self.request.id
            timemachine.save()

            rp = replayer.classes.ReplayManager(timemachine=timemachine)

            # load_db=False runs whats already in the replayer.models.Update table
            mode = timemachine.playback_mode
            if mode == TimeMachine.PLAYBACK_MODE_PLAY_ALL:
                #
                rp.play(load_db=False)

            elif mode == TimeMachine.PLAYBACK_MODE_PLAY_TO_TARGET:
                #
                rp.play(load_db=False, start_from=timemachine.start, play_until=timemachine.target)

        finally:
            release_lock()

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