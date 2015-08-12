from __future__ import absolute_import

from mysite.celery_app import app
from django.core.cache import cache
import contest.models

LOCK_EXPIRE = 60 # Lock expires in 5 minutes
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

    lock_id = '%s-LOCK-[%s]'%(SHARED_LOCK_NAME, draft_group.pk)

    acquire_lock = lambda: cache.add(lock_id, True, LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        #print('got lock')
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
            __on_game_closed( draft_group )

        finally:
            release_lock()
    else:
        #print('could not get lock')
        self.retry(countdown=3, max_retries=100)

def __on_game_closed( draft_group ):
    """
    this method should only be called inside of the lock in on_game_closed()
    """

    # get all the Games
    b = True  # default
    for g in draft_group.get_games():
        # AND each game with True
        b = b and g.is_closed()

    # b will be True when all the games are closed!
    if b:
        #
        # update all Contest's with this draft_group, to be completed
        Contest = contest.models.Contest
        contests = Contest.objects.filter( draft_group=draft_group ).exclude( status__in=Contest.STATUS_HISTORY )
        num_updated = contests.update( status=Contest.COMPLETED )
        print( str(num_updated), 'contests updated to status[%s]' % Contest.COMPLETED )
