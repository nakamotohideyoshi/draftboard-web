#
# replayer/admin.py

from django.utils.html import format_html
from django.contrib import admin
import replayer.models
from .tasks import load_replay, reset_db_for_replay
# change the datetime to show seconds for replayer/admin.py
from django.conf.locale.en import formats as en_formats
en_formats.DATETIME_FORMAT = "d b Y H:i:s"

@admin.register(replayer.models.Replay)
class ReplayAdmin(admin.ModelAdmin):
    list_display = ['name','start','end']

@admin.register(replayer.models.Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ['ts','ns','o']

@admin.register(replayer.models.TimeMachine)
class TimeMachineAdmin(admin.ModelAdmin):
    #
    # task statuses
    # In [13]: task.status
    # Out[13]: 'STARTED'
    #
    # In [14]: task.status
    # Out[14]: 'SUCCESS'

    #
    #  playback_mode is like "play-until-end" or "paused"
    list_display = ['replay', 'status', 'playback_mode', 'start', 'current', 'target' ]
    exclude = ('loader_task_id','playback_task_id')

    # use the fields which we are explicity stating in the Meta class
    fieldsets = (
        #
        ('Replay Settings', {
            'fields': (
                'replay',
                'playback_mode',
                'start',
                'target',
            )
        }),

        #
        # these fields are purposely collapsed,
        # and the form takes care of setting
        # them to default values.
        ('ignore these fields', {
            'classes' : ('collapse',),
            'fields': (

                'current',
            )
        }),
    )

    def status(self, obj):
        """
        Add a button into the admin views so its
        more intuitive to start the replay,
        (as opposed to having to save the object).

        :param obj:   the model instance for each row
        :return:
        """

        load_task_status = 'unknown'
        if obj.loader_task_id is None:
            load_task_status = 'ready for playback'
        else:
            result = load_replay.AsyncResult(obj.loader_task_id)
            if 'SUCCESS' in result.status:
                load_task_status = 'STOPPED'
            elif 'PENDING' in result.status:
                load_task_status = 'RUNNING'
            elif 'ABORTED' in result.status:
                load_task_status = 'STOPPED'
            else:
                load_task_status = result.status

        # the {} in the first argument are like %s for python strings,
        # and the subsequent arguments fill the {}
        return format_html('<a href="{}={}" class="btn btn-success">{}</a>',
                            "/admin/replayer/timemachine/",
                             obj.pk,
                             load_task_status)

    def start_replayer(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(request, 'You may only perform this action on one Replay at a time.')
        else:
            for obj in queryset:
                result = load_replay.delay( obj )     # the filename - i forget if path is prefixed!
                obj.loader_task_id = result.id
                print('loader_task_id: %s' % obj.loader_task_id)
                obj.current = None # zero out current on start (it will be set once it starts running
                obj.save()

    def stop_replayer(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(request, 'You may only perform this action on one Replay at a time.')
            return

        # there should be <= 1 obj's in here, but loop anyways
        for obj in queryset:
            #
            # get the task
            if obj.loader_task_id is None:
                return
            else:
                result = load_replay.AsyncResult(obj.loader_task_id)
                result.abort()

    def save_snapshot(self, request, queryset):
        task_result = reset_db_for_replay.delay()

    actions = [start_replayer, stop_replayer, save_snapshot]

