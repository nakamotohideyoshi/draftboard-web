#
# contest/schedule/classes.py

from django.utils import timezone
from django.db.transaction import atomic
from .models import Schedule, TemplateContest, ScheduledTemplateContest

class ScheduleManager(object):

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
            self.schedule_model     = schedule_model     # TODO TOOD TOOD  - we changed some models
            self.template_contests  = TemplateContest.objects.filter(schedule=self.schedule_model)
            self.scheduled_contests = ScheduledTemplateContest.objects.filter()

        def update(self):
            """
            creates new live Contests for scheduled contests which need to be created

            the process is essentially this:

                1) get all the TemplateContest objects for the WEEKDAY
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
            s = Schedule( sched )
            s.update() # run this schedule
