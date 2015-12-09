#
# replayer/admin.py

from django.utils.html import format_html
from django.contrib import admin
import replayer.models
import replayer.tasks

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
    list_display = ['replay', 'load_status', 'fill_contest_status', 'playback_status', 'playback_mode', 'start', 'current', 'target' ]
    exclude = ('loader_task_id','fill_contests_task_id','playback_task_id')

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

    # def status(self, obj):
    #     """
    #     Add a button into the admin views so its
    #     more intuitive to start the replay,
    #     (as opposed to having to save the object).
    #
    #     :param obj:   the model instance for each row
    #     :return:
    #     """
    #
    #     load_task_status = 'unknown'
    #     if obj.loader_task_id is None:
    #         load_task_status = 'ready for playback'
    #     else:
    #         result = load_replay.AsyncResult(obj.loader_task_id)
    #         if 'SUCCESS' in result.status:
    #             load_task_status = 'STOPPED'
    #         elif 'PENDING' in result.status:
    #             load_task_status = 'RUNNING'
    #         elif 'ABORTED' in result.status:
    #             load_task_status = 'STOPPED'
    #         else:
    #             load_task_status = result.status
    #
    #     # the {} in the first argument are like %s for python strings,
    #     # and the subsequent arguments fill the {}
    #     return format_html('<a href="{}={}" class="btn btn-success">{}</a>',
    #                         "/admin/replayer/timemachine/",
    #                          obj.pk,
    #                          load_task_status)

    def load_initial_database(self, request, queryset):
        """
        pull down the snapshot db for the stats replayer BEFORE the stats started being recorded
        so the database is back in time, and the admin can modify things on the site
        before starting the stats.

        :param request:
        :param queryset:
        :return:
        """
        if len(queryset) > 1:
            self.message_user(request, 'You may only perform this action on one Replay at a time.')
            return

        # TODO the queryset should have 1 object in it, and that object has the name of the snapshot to load from s3
        for timemachine in queryset:
            print('TODO - load_initial_database load bad replay file right now')
            task_result = replayer.tasks.reset_db_for_replay.delay(timemachine.replay)

            timemachine.loader_task_id=task_result.id
            timemachine.save()

    def fill_existing_contests(self, request, queryset):
        """
        fill all existing contests on the site with entries.

        if you want some contests that are not filled entirely, add them after running this action

        :param request:
        :param queryset:
        :return:
        """
        if len(queryset) > 1:
            self.message_user(request, 'You may only perform this action on one Replay at a time.')
            return

        for timemachine in queryset:
            task_result = replayer.tasks.fill_contests.delay( timemachine )

            timemachine.fill_contests_task_id=task_result.id
            timemachine.save()

    def start_replayer(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(request, 'You may only perform this action on one Replay at a time.')
            return

        for timemachine in queryset:
            timemachine.playback_status = None
            timemachine.current         = None # zero out current on start (it will be set once it starts running
            timemachine.save()
            timemachine.refresh_from_db()

            result = replayer.tasks.play_replay.delay( timemachine )     # the filename - i forget if path is prefixed!
            timemachine.loader_task_id = result.id
            print('loader_task_id: %s' % timemachine.loader_task_id)

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
                result = replayer.tasks.play_replay.AsyncResult(obj.loader_task_id)
                result.abort()

    actions = [load_initial_database, fill_existing_contests, start_replayer, stop_replayer]

