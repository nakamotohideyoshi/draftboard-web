from __future__ import absolute_import

#
# mysite/tasks.py

from mysite.celery_app import app
from datetime import timedelta
from django.utils import timezone
from contest.models import LiveContest

#
# very important/required notify email list
HIGH_PRIORITY_EMAILS = [
    'cbanister@coderden.com',
    'manager@draftboard.com'
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
def recalculate_user_loyalty():
    pass # TODO

#
#########################################################################
# admin
#########################################################################

#
# check if there are user withdraw requests which need to be processed,
# and email the appropriate list of people if there are.
def check_pending_withdraws():
    pass # TODO

# #
# # example: send an email report including the name and
# #           information of all the signups from a time period
# def email_daily_user_signups_EXAMPLE():
#     pass # TODO

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
    pass # TODO

#
# based on the time it is, make sure there are no Contests
# that should have started, but whose statuses remain
# in ANY kind of registering/pregame state, and email
# all admin asap if there is an issue.
@app.task
def validate_daily_contests_started():
    #print( 'validate_daily_contests_started' )
    pass # TODO

#
# if it 'hours' past the start time of the latest
# game in the draft_group, notifiy admins to check
# to make sure things are running as intended.
#
# this situation may arise from a postponed/delayed
# game or stat provider issue.
@app.task(bind=True)
def validate_daily_contests_paid(self, *args, **kwargs):
    #print( 'validate_daily_contests_paid' )
    # print( str(args) )
    #
    # print( str(args) )
    # for k,v in kwargs.items():
    #     print( str(k), ':', str(v) )

    # if we check on the live contests, in any early AM timezone,
    # we should be cautious about any that are still live because
    # typically contests finish by now.
    red_flag_contests = LiveContest.objects.all()
    print( len(red_flag_contests), 'contests still live!')

#
#########################################################################
# NFL
#########################################################################

#
#
def nfl_task():
    pass # TODO

#
#########################################################################
# NBA
#########################################################################

#
#
def nba_task():
    pass # TODO

#
#########################################################################
# NHL
#########################################################################

#
#
def nhl_task():
    pass # TODO

#
#########################################################################
# MLB
#########################################################################

#
#
def mlb_task():
    pass # TODO


