#
# push/tasks.py

from __future__ import absolute_import

from mysite.celery_app import app

@app.task(bind=True)
def pusher_send_task(self, pushable, data):
    pushable.send( data )




