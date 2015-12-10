#
# replayer/admin.py

from mysite import celery_app as app            # app.revoke( <task-id>, terminate=True, signal='SIGKILL' )
from django.utils.html import format_html
from django.contrib import admin
import replayer.models
import replayer.tasks
from datetime import timedelta
from util.timeshift import set_system_time, reset_system_time
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
    list_display = ['replay', 'load_status', 'fill_contest_status', 'playback_status', 'playback_mode', 'start', 'current', 'target', 'snapshot_datetime' ]
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
                'snapshot_datetime',
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
        resets util.timeshift delta before loading snapshot db

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

        for timemachine in queryset:
            print('resetting timeshift with util.timeshift.reset_system_time()')
            reset_system_time()

            task_result = replayer.tasks.reset_db_for_replay.delay(timemachine.replay)

            timemachine.load_status  = 'LOADING...'
            timemachine.fill_contest_status = 'PLEASE REFRESH BROWSER & LOG BACK IN'
            timemachine.playback_status = ''
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

            # start the replay task
            result = replayer.tasks.play_replay.delay( timemachine )     # the filename - i forget if path is prefixed!

            timemachine.refresh_from_db()
            timemachine.playback_task_id = result.id
            print('playback_task_id: %s' % timemachine.playback_task_id)
            timemachine.save()

            print('playback_task status: %s' % result.status)

    def stop_replayer(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(request, 'You may only perform this action on one Replay at a time.')
            return

        # there should be <= 1 obj's in here, but loop anyways
        for timemachine in queryset:
            kill_task_id = timemachine.playback_task_id
            if kill_task_id is None:
                print('there was no playback_task_id set, couldnt stop it if its running!')
            else:
                print('STOPPING replayer playback task forcibly!')
                app.control.revoke( kill_task_id, terminate=True, signal='SIGKILL' )

                timemachine.playback_status = 'KILLED'
                timemachine.save()

    # def shift_server_time_to_replay_time(self, request, queryset):
    #     if len(queryset) > 1:
    #         self.message_user(request, 'You may only perform this action on one Replay at a time.')
    #         return
    #     for timemachine in queryset:
    #         #
    #         initial_datetime = timemachine.snapshot_datetime
    #         print('using timeshift.set_system_time( %s )' % str(initial_datetime))
    #         set_system_time( initial_datetime )

    def set_time_one_hour_before_replay_start(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(request, 'You may only perform this action on one Replay at a time.')
            return

        updates = replayer.models.Update.objects.filter().order_by('ts') # ascending
        if updates.count() <= 0:
            self.message_user(request, 'There are no replayer.models.Update objects!')
            return

        first_update = updates[0] # first one is earlier, because we sorted
        dt_set_time = first_update.ts - timedelta(hours=1)
        set_system_time( dt_set_time )
        print( 'set_system_time( %s )' % str(dt_set_time) )

    actions = [load_initial_database, set_time_one_hour_before_replay_start, fill_existing_contests, start_replayer, stop_replayer]

