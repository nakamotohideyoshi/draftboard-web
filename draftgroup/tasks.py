from __future__ import absolute_import

from logging import getLogger

from django.core.cache import cache
from django.utils import timezone

import contest.models
from mysite.celery_app import app

logger = getLogger('draftgroup.tasks')

LOCK_EXPIRE = 60  # Lock expires in 5 minutes
SHARED_LOCK_NAME = "draftgroup_task__on_game_closed"


@app.task(bind=True)
def on_game_closed(self, draft_group):
    """
    Updates the Contest(s) with this DraftGroup
    to be complete (ie: ready to be paid out)
    if ALL the games in the draft_group are closed.

    This task will likely be called for each Game
    as it gets closed.

    It is important that this task be unique PER DRAFTGROUP.
    """

    lock_id = '%s-LOCK-[%s]' % (SHARED_LOCK_NAME, draft_group.pk)

    acquire_lock = lambda: cache.add(lock_id, True, LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        # print('got lock')
        try:
            # dgm = DraftGroupManager()
            # # get all the Games
            # games = dgm.get_games( draft_group=draft_group )
            # b = True  # default
            # for g in games:
            #     # AND each game with True
            #     b = b and g.is_closed()
            #
            # # b will be True when all the games are closed!
            # if b:
            #     #
            #     # update all Contest's with this draft_group, to be completed
            #     Contest.objects.filter( draft_group=draft_group ).update( status=Contest.COMPLETED )
            __on_game_closed(draft_group)

        finally:
            release_lock()
    else:
        # print('could not get lock')
        self.retry(countdown=3, max_retries=100)


def __on_game_closed(draft_group):
    """
    this method should only be called inside of the lock in on_game_closed()
    """

    logger.info(
        'A game has closed, checking if contests in draftgroup should also close. %s'
        % draft_group
    )

    # get all the Games
    b = True  # default
    for g in draft_group.get_games():
        # AND each game with True
        b = b and g.is_closed()

    # b will be True when all the games are closed!
    if b:
        #
        # set the datetime to the draft group so we know when all games closed
        draft_group.closed = timezone.now()
        draft_group.save()

        #
        # update all Contest's with this draft_group, to be completed
        Contest = contest.models.Contest
        contests = Contest.objects.filter(draft_group=draft_group).exclude(
            status__in=Contest.STATUS_HISTORY)
        num_updated = contests.update(status=Contest.COMPLETED)
        from contest.tasks import track_contests
        track_contests.delay(contests)
        logger.info('%s contests updated to status[%s]' % (
            num_updated, Contest.COMPLETED))


@app.task(bind=True)
def on_game_inprogress(self, draft_group):
    """
    checks to see if there are any Contests that need to be
    cancelled and refunded every time a live game goes to "inprogress"

    Contests which are not guaranteed prize pools (contest.gpp=True),
    must fill up before their start time, or they will
    be cancelled and refunded by this task.
    """
    import contest.refund.tasks
    contests = contest.models.LiveContest.objects.filter(gpp=False)
    refund_task_results = []
    for c in contests:
        if not c.is_filled():
            #
            # call the refund_task with the contest
            res = contest.refund.tasks.refund_task.delay(c)

            #
            # create a list of tuples, of pairs of (DraftGroup, taskresult)
            refund_task_results.append((draft_group, res))
