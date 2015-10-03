web: newrelic-admin run-program gunicorn --pythonpath mysite mysite.wsgi -b 0.0.0.0:$PORT --workers $GUNICORN_WORKERS --max-requests $GUNICORN_MAX_REQUESTS --timeout $GUNICORN_TIMEOUT

#
# runs the celerybeat scheduled tasks from the CELERYBEAT_SCHEDULE
# which should be found in mysite.celery_app.py
celerybeat: celery -A mysite beat -S djcelery.schedulers.DatabaseScheduler

#
# a worker for misc, very short-lived tasks (ie: milliseconds, hopefully).
#
# this worker always wipes out the brokers existing/pending tasks on startup.
# without startup purge, its possible we will have WAY too to consume initially.
celery: celery -A mysite worker -l info --purge

#
# the mandatory (and the only) worker responsible for running dataden.
# no other worker should consume from the queue this worker consumes from
dataden: celery -A mysite worker -l info -Q q_dataden --purge

#
# the mandatory (and the only) worker responsible for running dataden triggers
# on the mongo database. this task ensures data is being pushed from mongo to django/postgres.
# no other worker should consume from the this worker consumes from
dataden_trigger: celery -A mysite worker -l info -Q q_dataden_trigger --purge
