from __future__ import absolute_import

#
# mysite/tasks.py

from mysite.celery_app import app
from datetime import timedelta
from django.utils import timezone
from contest.models import LiveContest, Contest, UpcomingContest
from draftgroup.models import DraftGroup, UpcomingDraftGroup
from django.core.mail import send_mail
from rakepaid.classes import LoyaltyStatusManager

#
#
HIGH_PRIORITY_FROM_EMAIL = 'admin@draftboard.com'
LOW_PRIORITY_FROM_EMAIL = 'admin@draftboard.com'


#
# very important/required notify email list
HIGH_PRIORITY_EMAILS = [
    'cbanister@coderden.com',
    'manager@draftboard.com',
    'pedro@draftboard.com',
]

#
# for stuff that isnt life-or-death.
LOW_PRIORITY_EMAILS = [
    'cbanister@coderden.com'
]

#
#########################################################################
# miscellaneous
#########################################################################

#
# at some point in the evening, just after all contests
# have been paid out, we need to recalculate every users
# loyalty status. we must do this for all users
# because everyone is on a 30 day rolling window.
@app.task(bind=True)
def recalculate_user_loyalty():
    loyalty_status_manager = LoyaltyStatusManager()
    loyalty_status_manager.update()

#
#########################################################################
# admin
#########################################################################

#
#########################################################################
# contests
#########################################################################

#
# check if we are getting within a few days of any contests
# which dont have a draft_group set. (this implies the contests
# were allowing early registration.)
#
# notifiy someone to remind them to create the draft group asap!
@app.task
def notifiy_admin_contests_require_draft_group():
    td = timedelta(days=7)
    target = timezone.now() + td
    contests = UpcomingContest.objects.filter( draft_group__isnull=True, start__lte=target)
    contests_str = str([ str(c.name) for c in contests])

    send_mail("Alert! Upcoming Contests need a Draft-Group!",
                contests_str,
                HIGH_PRIORITY_FROM_EMAIL,
                HIGH_PRIORITY_EMAILS)

#
# based on the time it is, make sure there are no Contests
# that should have started, but whose statuses remain
# in ANY kind of registering/pregame state, and email
# all admin asap if there is an issue.
@app.task
def validate_daily_contests_started():
    #print( 'validate_daily_contests_started' )
    pass # TODO

@app.task(bind=True)
def notify_admin_draft_groups_not_completed(self, hours=5, *args, **kwargs):
    """
    We know when a DraftGroup's last game starts, but we dont know
    when it will end.

    We should notify an admin if its been 5 hours since the last
    game started, but the DraftGroup is still not closed,
    because most games never take that long.

    *** This task looks at DraftGroup(s) in the last 15 days.

    :param hours:
    :param args:
    :param kwargs:
    :return:
    """
    days_back           = 15
    now                 = timezone.now()
    start_lookup_range  = now - timedelta(days=days_back)
    end_lookup_range    = now - timedelta(hours=hours)

    #
    # Get the DraftGroup(s) that havent been closed yet
    draft_groups    = DraftGroup.objects.filter(end__gte=start_lookup_range,
                                                end__lte=end_lookup_range,
                                                closed__isnull=True)

    #
    contests = Contest.objects.filter( draft_group__in=draft_groups )

    msg_str = '*** %s *** contests are live >>> %s <<< hours after the last game(s) started.' % (contests.count(), hours)
    print(msg_str )
    send_mail("Alert! Draft Groups (Live Games) Running late (!?)",
                msg_str,
                HIGH_PRIORITY_FROM_EMAIL,
                HIGH_PRIORITY_EMAILS)


@app.task(bind=True)
def notify_admin_contests_not_paid(self, *args, **kwargs):
    """
    If a Contest is in the 'completed' state, it needs to be paid out!

    This task notifies an admin of ANY Contests in the 'completed' state.

    This task can be run on a ~15 minute interval

    :param args:
    :param kwargs:
    :return:
    """
    payable_contests = Contest.objects.filter(status=Contest.COMPLETED)
    num_contests = payable_contests.count()
    if num_contests > 0:
        msg_str = '*** %s *** need to be paid out!' % (num_contests)
        print( msg_str )

        send_mail("Alert! Contest Payout time!",
                    msg_str,
                    HIGH_PRIORITY_FROM_EMAIL,
                    HIGH_PRIORITY_EMAILS)