#
# replayer/models.py

from django.db import models
from django.conf import settings

class Replay(models.Model):
    created     = models.DateTimeField(auto_now_add=True, null=False)
    name        = models.CharField(max_length=256, null=False)

    start       = models.DateTimeField(null=False)
    end         = models.DateTimeField(null=True)    # it has not ended yet.

class Update(models.Model):

    # the timestamp when this update happened in actual real-time
    ts = models.DateTimeField(null=False)

    # the namespace this Update was triggered from -- the dot separated
    # mongo db.colletion. for example, this is a namespace: "nba.game"
    ns  = models.CharField(max_length=64, null=False)

    # the dictionary object dumped to a string, which contains the update data
    o   = models.CharField(max_length=8192, null=False)

class TimeMachine(models.Model):

    # LOADING_STATUSES = [
    #     ('todo-status','TODO-LOADING-STATUS')
    # ]
    #
    # PLAYBACK_STATUSES = [
    #     ('todo-status','TODO-PLAYBACK-STATUS')
    # ]

    PLAYBACK_MODE_PLAY_ALL          = 'play-all'
    PLAYBACK_MODE_PLAY_TO_TARGET    = 'play-to-target'

    PLAYBACK_MODES = [
        (PLAYBACK_MODE_PLAY_ALL,        'Play All'),
        (PLAYBACK_MODE_PLAY_TO_TARGET,  'Play to Target'),
    ]

    # the id of the celery task that will load the replay into the Update table (takes 0-30 seconds usually)
    loader_task_id          = models.CharField(max_length=255, default=None, null=True)
    fill_contests_task_id   = models.CharField(max_length=255, default=None, null=True)
    playback_task_id        = models.CharField(max_length=255, default=None, null=True)

    load_status             = models.CharField(max_length=64, default=None, null=True)
    fill_contest_status     = models.CharField(max_length=64, default=None, null=True)
    playback_status         = models.CharField(max_length=64, default=None, null=True)

    replay          = models.CharField(max_length=255, null=False, default='',
                                    help_text='the name of the replay (a postgres dump) on s3')
    #replay          = models.FilePathField(path=settings.SMUGGLER_FIXTURE_DIR)

    # loading_status  = models.CharField(max_length=255, null=False, default='',
    #                     choices=LOADING_STATUSES,
    #                     help_text='status of replay. initial -> loading -> playing')
    # playback_status = models.CharField(max_length=255, null=False, default='',
    #                     choices=PLAYBACK_STATUSES,
    #                     help_text='status of replay. initial -> loading -> playing')
    start           = models.DateTimeField(null=False,
                        help_text='the time you want to start at in the replay. must be within the start and end of the recorded stats')
    current         = models.DateTimeField(null=True, blank=True,
                        help_text='where the replay is currently')
    target          = models.DateTimeField(null=True, blank=True,
                        help_text='SET THE STOP TARGET FOR PLAY-TO-TARGET mode. the time you want to start at in the replay. must be within the start and end of the recorded stats')
    playback_mode   = models.CharField(max_length=64, null=False, choices=PLAYBACK_MODES )

    snapshot_datetime = models.DateTimeField(null=True, blank=True,
                                             help_text='internal field for settings the time to rewind the server to when the replay dump is re-loaded.')
