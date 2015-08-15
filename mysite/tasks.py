# from __future__ import absolute_import
#
# #
# # mysite/tasks.py
#
# from .celery_app import app
#
# #
# # very important/required notify email list
# HIGH_PRIORITY_EMAILS = [
#     'cbanister@coderden.com',
#     'manager@draftboard.com'
# ]
#
# #
# # for stuff that isnt life-or-death.
# LOW_PRIORITY_EMAILS = [
#     'cbanister@coderden.com'
# ]
#
# #
# #########################################################################
# # miscellaneous
# #########################################################################
#
# #
# # at some point in the evening, just after all contests
# # have been paid out, we need to recalculate every users
# # loyalty status. we must do this for all users
# # because everyone is on a 30 day rolling window.
# def recalculate_user_loyalty():
#     pass # TODO
#
# #
# #########################################################################
# # admin
# #########################################################################
#
# #
# # check if there are user withdraw requests which need to be processed,
# # and email the appropriate list of people if there are.
# def check_pending_withdraws():
#     pass # TODO
#
# # #
# # # example: send an email report including the name and
# # #           information of all the signups from a time period
# # def email_daily_user_signups_EXAMPLE():
# #     pass # TODO
#
# #
# #########################################################################
# # contests
# #########################################################################
#
# #
# # based on the time it is, make sure there are no Contests
# # that should have started, but whose statuses remain
# # in ANY kind of registering/pregame state, and email
# # all admin asap if there is an issue.
# @app.task(bind=True)
# def validate_daily_contests_started():
#     print( 'validate_daily_contests_started' )
#
# #
# # if its a long time after games usually pay out,
# # and they havent paid out yet.... we should email
# # the people who can fix this situation.
# #
# # the situation may arise from a postponed/delayed
# # game or stat provider issue.
# @app.task(bind=True)
# def validate_daily_contests_paid():
#     print( 'validate_daily_contests_paid' )
#
# #
# #########################################################################
# # NFL
# #########################################################################
#
# #
# #
# def nfl_task():
#     pass # TODO
#
# #
# #########################################################################
# # NBA
# #########################################################################
#
# #
# #
# def nba_task():
#     pass # TODO
#
# #
# #########################################################################
# # NHL
# #########################################################################
#
# #
# #
# def nhl_task():
#     pass # TODO
#
# #
# #########################################################################
# # MLB
# #########################################################################
#
# #
# #
# def mlb_task():
#     pass # TODO