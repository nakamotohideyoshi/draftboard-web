#
# push/tasks.py

from __future__ import absolute_import

from mysite.celery_app import app
from django.core.cache import cache

@app.task(bind=True)
def pusher_send_task(self, pushable, data):
    pushable.trigger( data )

# TODO - make this task blocking wait for the same lock the pusher.classes.AbstractPush.Linker uses to add to cache
@app.task(bind=True)
def linker_pusher_send_task(self, pushable, data, identifier):
    # atomically delete the identifier from the cache.
    # delete() returns > 0 if it deleted something.
    # if it didnt, that means no identifier existed,
    # and that means we dont need to send the data.
    if cache.delete(identifier) == 0:
        return # the identifier token didnt exist, so we dont need to send it

    # now we know we have to send the data, since we deleted something
    pushable.trigger( data )

    # TODO - remove the object with the identifier from the linked queue in the cache too!




