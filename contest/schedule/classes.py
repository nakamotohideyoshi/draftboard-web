#
# contest/schedule/classes.py

from django.utils import timezone
from django.db.transaction import atomic
from django.db.models import Q
from .models import Schedule, TemplateContest, ScheduledTemplateContest

class ScheduleManager(object):
    """
    Schedule                    - master entry, which many ScheduledTemplateContest(s) point to
    TemplateContest             - information to be able to clone a Contest
    ScheduledTemplateContest    - the map between a TemplateContest + Schedule
    """

    NOW_FORMAT = '%Y-%m-%d %H:%M:%S'

    class Schedule(object):

        def __init__(self, schedule_model, dt=None):
            """

            :param schedule_model: the schedule for which we will get
                        TemplateContest objects, and create corresponding Contests if necessary
            :param dt: datetime object, if None we use the current time to decide what to schedule
            :return:
            """
            self.now = dt
            if dt is None:
                self.now = timezone.now()

            self.schedule_model     = schedule_model
            self.scheduled_contests = self.get_scheduled_template_contests( self.now )

            # debug print the scheduled_contests we find
            for sc in self.scheduled_contests:
                print( sc )

        def get_scheduled_template_contests(self, dt):
            """
            get all the ScheduledTemplateContest objects for the the datetime object dt

            :param dt:
            :return:
            """

            # TODO TODO we need to decide when to schedule upcoming games (~3 hours before start of todays games?)
            weekday = dt.weekday() # the current weekday of the server
            q = None
            if weekday == 0: q = Q(interval__monday=True)
            elif weekday == 1: q = Q(interval__tuesday=True)
            elif weekday == 2: q = Q(interval__wednesday=True)
            elif weekday == 3: q = Q(interval__thursday=True)
            elif weekday == 4: q = Q(interval__friday=True)
            elif weekday == 5: q = Q(interval__saturday=True)
            elif weekday == 6: q = Q(interval__sunday=True)
            else: raise Exception('weekday is not in the range [0-6]!')

            return ScheduledTemplateContest.objects.filter( q, schedule=self.schedule_model )

        def update(self):
            """
            creates new live Contests for scheduled contests which need to be created

            the process is essentially this:

                1) get all the ScheduledTemplateContest objects for the WEEKDAY
                2) for each template
                    a) if there is a record showing we already
                        created it (ScheduledContest entry), do nothing
                    b) else: atomically create a new ScheduledContest entry,
                        and also create the actual Contest
            """
            pass

    def __init__(self):
        self.schedules = Schedule.objects.all()

    def now_str(self):
        return timezone.now().strftime(self.NOW_FORMAT)

    def print_schedules(self):
        print('today is:', self.now_str() )
        print('----schedules----')
        for sched in self.schedules:
            print( sched )

    def run(self):
        """
        Create Contests which need to be scheduled, and have not yet been created.

        This method can be run as often as necessary.

        :return:
        """

        for sched in self.schedules:
            sc = self.Schedule( sched )
            sc.update() # run this schedule
