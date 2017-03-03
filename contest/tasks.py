from __future__ import absolute_import

from datetime import timedelta
from logging import getLogger

from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone

from contest.classes import ContestPoolFiller
from contest.models import (
    Contest,
    CompletedContest,  # can pay these out
    LiveContestPool,  # in this state, all of its Contests should be created
)
from contest.payout.models import Payout
from contest.payout.tasks import payout_task
from draftgroup.models import DraftGroup
from mysite.celery_app import app
from mysite.kissmetrics import track_contest_end
from rakepaid.classes import LoyaltyStatusManager
from util.slack import WebhookContestInfo

logger = getLogger('contests.tasks')
HIGH_PRIORITY_FROM_EMAIL = 'admin@draftboard.com'
LOW_PRIORITY_FROM_EMAIL = 'admin@draftboard.com'

#
# very important/required notify email list
HIGH_PRIORITY_EMAILS = [
    'devs@draftboard.com',
    'manager@draftboard.com',
]

#
# for stuff that isnt life-or-death.
LOW_PRIORITY_EMAILS = [
    'devs@draftboard.com'
]

LOCK_EXPIRE = 60  # lock expires in this many seconds
SHARED_LOCK_NAME = 'spawn_contest_pool_contests'

slack = WebhookContestInfo()


@app.task(bind=True)
def spawn_contest_pool_contests(self):
    lock_id = 'task-LOCK--%s--%s' % ('all_sports', SHARED_LOCK_NAME)

    acquire_lock = lambda: cache.add(lock_id, 'lock', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:
            contest_pools = LiveContestPool.objects.all()
            for cp in contest_pools:
                msg = "🏁 Attempting to spawn contests from ContestPool: ```%s```" % cp
                logger.info(msg)
                slack.send(msg)
                cpf = ContestPoolFiller(cp)
                # create all its Contests using FairMatch
                new_contests = cpf.fair_match()
                for new_contest in new_contests:
                    msg = "> 🐥 Spawned ```%s```" % new_contest
                    logger.info(msg)
                    slack.send(msg)
        finally:
            release_lock()


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
# based on the time it is, make sure there are no Contests
# that should have started, but whose statuses remain
# in ANY kind of registering/pregame state, and email
# all admin asap if there is an issue.
@app.task
def validate_daily_contests_started():
    # print( 'validate_daily_contests_started' )
    pass  # TODO


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
    days_back = 15
    now = timezone.now()
    start_lookup_range = now - timedelta(days=days_back)
    end_lookup_range = now - timedelta(hours=hours)

    #
    # Get the DraftGroup(s) that havent been closed yet
    draft_groups = DraftGroup.objects.filter(end__gte=start_lookup_range,
                                             end__lte=end_lookup_range,
                                             closed__isnull=True)

    #
    contests = Contest.objects.filter(draft_group__in=draft_groups)

    msg_str = (
                  '%s contests are live >>> %s <<< hours after the last game(s) started. It\'s been %s hours '
                  'since the last game started, but the DraftGroup is still not closed, because most games '
                  'never take that long.') % (contests.count(), hours, hours)
    for contest in contests:
        msg_str += '\n  %s' % contest

    logger.info(msg_str)
    slack.send(msg_str)
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
        msg_str = '%s contests need to be paid out!' % (num_contests)
        for contest in payable_contests:
            msg_str += '\n\t%s' % contest

        logger.info(msg_str)

        slack.send("Alert! Contest Payout time! %s" % msg_str)
        send_mail("Alert! Contest Payout time!",
                  msg_str,
                  HIGH_PRIORITY_FROM_EMAIL,
                  HIGH_PRIORITY_EMAILS)


@app.task(bind=True)
def notify_admin_contests_automatically_paid_out(self, *args, **kwargs):
    """
    If a Contest is in the 'completed' state, it needs to be paid out!

    This task will do that - and then email the admin.

    :param args:
    :param kwargs:
    :return:
    """
    contests_to_pay = CompletedContest.objects.all()
    num_contests = contests_to_pay.count()

    #
    # use the payout_task to payout all completed contests
    task = payout_task.delay(contests=list(contests_to_pay))

    if contests_to_pay.count() > 0:
        msg_str = '💰 %s completed contests have automatically paid out:\n\n' % num_contests
        for contest in contests_to_pay:
            msg_str += '```%s``` \n' % contest
        logger.info(msg_str)
        slack.send(msg_str)
        send_mail(
            subject="Contest Auto Payout Time!",
            message=msg_str,
            html_message="Contest Auto Payout Time!",
            from_email=HIGH_PRIORITY_FROM_EMAIL,
            recipient_list=HIGH_PRIORITY_EMAILS,
        )


@app.task
def track_contests(contests):
    """
    Send an analytics event to Kissmetrics with contest data.

    Args:
        contests: List of Contest objects

    Returns: None
    """
    for contest in contests:
        base_data = {
            'Total Fees/Money Entered': contest.prize_structure.prize_pool,
            'Sport': contest.sport,
            'Total Entries': contest.current_entries,
            'Contest Type': contest.prize_structure.get_format_str(),
        }
        users = [x.user for x in contest.contests.distinct('user')]
        for user in users:
            payment = Payout.objects.filter(entry__contest=contest,
                                            entry__user=user).first()
            data = base_data.copy()
            data.update({
                'Total Lineups': contest.contests.filter(user=user).count(),
                'In Money': True if payment else False,
            })
            if payment:
                data['Money Won'] = payment.amount
                data['Place'] = payment.rank
            track_contest_end(user.username, data)
