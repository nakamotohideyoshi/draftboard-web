#
# replayer/admin.py

from django.utils.html import format_html
from django.contrib import admin
import replayer.models
from .tasks import load_replay

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
    list_display = ['replay', 'status', 'playback_mode', 'start', 'current' ]
    exclude = ('loader_task_id','playback_task_id')

    # use the fields which we are explicity stating in the Meta class
    fieldsets = (
        #
        ('Replay Settings', {
            'fields': (
                'replay',
                'playback_mode',
                'start',
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
            load_task_status = 'Unknown'
        else:
            result = load_replay.AsyncResult(obj.loader_task_id)
            if 'SUCCESS' in result.status:
                load_task_status = 'FINISHED'
            elif 'PENDING' in result.status:
                load_task_status = 'RUNNING'
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
            self.message_user(request, 'You may only select one Replay at a time.')
        else:
            for obj in queryset:
                task = load_replay.delay( obj )     # the filename - i forget if path is prefixed!
                obj.loader_task_id = task.id
                print('loader_task_id: %s' % obj.loader_task_id)
                obj.save()

    actions = [start_replayer, ]

