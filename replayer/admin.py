#
# replayer/admin.py

from ast import literal_eval
from datetime import timedelta

import requests
from django.contrib import admin
from django.utils.html import format_html
from django_celery_beat.models import PeriodicTask

import replayer.classes
import replayer.models
import replayer.tasks
from mysite import celery_app as app  # app.revoke( <task-id>, terminate=True, signal='SIGKILL' )
from util.timeshift import set_system_time, reset_system_time


# change the datetime to show seconds for replayer/admin.py
# from django.conf.locale.en import formats as en_formats
# #en_formats.DATETIME_FORMAT = "m/d/Y h:i:s P"
# en_formats.DATETIME_FORMAT = "m/d/Y P"

def enable_contest_pool_contest_spawner():
    # make sure the task that spawns ContestPool's Contest(s) is running
    pt = PeriodicTask.objects.get(name='generate_contest_pool_contests')
    # Set this tasks' last run time waaay back and enable it so that we ensure contests get spawned.
    pt.last_run_at = pt.last_run_at - timedelta(days=5000)
    pt.enabled = True
    pt.save()


@admin.register(replayer.models.Replay)
class ReplayAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'end']


@admin.register(replayer.models.Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ['id', 'delta', 'ts', 'ns', 'o']
    list_filter = ['ns']
    search_fields = ['id', 'ts', 'ns', 'o']

    def delta(self, update):
        # TODO - calculate the difference in seconds between the 'ts' field
        # of the model save() and the 'dd_updated__id' of the object
        o = literal_eval(update.o)
        o_ts = int(o.get('dd_updated__id')) / 1000
        ts = int(
            update.ts.strftime('%s')) - 5 * 60 * 60  # UTC will have to be modified when its -4 hrs
        # print('o_ts:', str(o_ts), 'ts:', str(ts))
        return str(int(ts - o_ts)) + ' sec'


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
    list_display = [
        'replay',
        # 'load_status',
        # 'fill_contest_status',
        'playback_status',
        'start',
        # 'playback_mode',
        # 'current',
        # 'snapshot_datetime',
        'playback_info',
        # 'target'
    ]

    exclude = ('loader_task_id', 'fill_contests_task_id', 'playback_task_id')

    # use the fields which we are explicity stating in the Meta class
    fieldsets = (
        #
        ('Replay Settings', {
            'fields': (
                'start',
            )
        }),

        #
        # these fields are purposely collapsed,
        # and the form takes care of setting
        # them to default values.
        ('ignore these fields', {
            'classes': ('collapse',),
            'fields': (
                'replay',
                'current',
                'snapshot_datetime',
                'playback_mode',
                'target',
            )
        }),
    )

    def playback_info(self, obj):
        """
        Add a button into the admin views so its
        more intuitive to start the replay,
        (as opposed to having to save the object).

        :param obj:   the model instance for each row
        :return:
        """

        playback_task_status = 'n/a'
        failed = False
        if obj.playback_task_id is None:
            pass
        else:
            playback_task_result = replayer.tasks.play_replay.AsyncResult(obj.playback_task_id)
            # playback_task_status = playback_task_result.status
            if playback_task_result.status == 'FAILURE':
                playback_task_status = "playback error - try it again"
                failed = True

        # the {} in the first argument are like %s for python strings,
        # and the subsequent arguments fill the {}
        btn_type = 'btn btn-success'
        if failed:
            btn_type = 'btn btn-warning'

        return format_html('<a href="{}" class="{}">{}</a>',
                           "/admin/replayer/timemachine/",
                           btn_type,
                           playback_task_status)

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

            timemachine.load_status = 'LOADING...'
            timemachine.fill_contest_status = 'PLEASE REFRESH BROWSER & LOG BACK IN'
            timemachine.playback_status = ''
            timemachine.loader_task_id = task_result.id
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
            task_result = replayer.tasks.fill_contests.delay(timemachine)

            timemachine.fill_contests_task_id = task_result.id
            timemachine.save()

    def start_replayer(self, request, queryset):
        #
        enable_contest_pool_contest_spawner()

        #
        if len(queryset) > 1:
            self.message_user(request, 'You may only perform this action on one Replay at a time.')
            return

        for timemachine in queryset:
            timemachine.playback_status = None
            timemachine.current = None  # zero out current on start (it will be set once it starts running
            timemachine.save()
            timemachine.refresh_from_db()

            # start the replay task
            result = replayer.tasks.play_replay.delay(
                timemachine)  # the filename - i forget if path is prefixed!

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
                app.control.revoke(kill_task_id, terminate=True, signal='SIGKILL')

                timemachine.playback_status = 'KILLED'
                timemachine.save()

    def set_time_one_hour_before_replay_start(self, request, queryset):
        """
        sets the system time to 1 hour before the first Update object (a stat of the replayer).

        also creates the default TicketAmount's and headsup PrizeStructures !

        :param request:
        :param queryset:
        :return:
        """
        #
        print('ensure default TicketAmount(s) and headsup PrizeStructures exist...')
        rp = replayer.classes.ReplayManager()
        rp.build_world()  # put initialization like making default tickets, and prize structures in this method!

        if len(queryset) > 1:
            self.message_user(request, 'You may only perform this action on one Replay at a time.')
            return

        updates = replayer.models.Update.objects.filter().order_by('ts')  # ascending
        if updates.count() <= 0:
            self.message_user(request, 'There are no replayer.models.Update objects!')
            return

        first_update = updates[0]  # first one is earlier, because we sorted
        dt_set_time = first_update.ts - timedelta(hours=1)
        set_system_time(dt_set_time)
        print('set_system_time( %s )' % str(dt_set_time))

    def reset_replay(self, request, querset):
        # forcibly calls the endpoint at the replayers remote controller ec2 server to reset the replay!
        session = requests.Session()
        r = session.post('http://54.172.56.78/api/replayer/reset-replay/')

    # actions = [load_initial_database, set_time_one_hour_before_replay_start, fill_existing_contests, start_replayer, stop_replayer]
    actions = [
        # load_initial_database,
        set_time_one_hour_before_replay_start,
        # fill_existing_contests,
        start_replayer,
        stop_replayer,
        reset_replay
    ]
