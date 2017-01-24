web: newrelic-admin run-program gunicorn --pythonpath mysite mysite.wsgi -b 0.0.0.0:$PORT --workers $GUNICORN_WORKERS --max-requests $GUNICORN_MAX_REQUESTS --timeout $GUNICORN_TIMEOUT


# Runs the celerybeat scheduled tasks that can be found in the Django admin panel.
celerybeat: celery -A mysite beat


# Standard celery worker.
celery: celery -A mysite worker -l info --autoscale=2,4 -n Standard@%n


# Long-running celery task queue for things like <sport>.cleanup_roster that take a while.
# soft time limit of 9 mins, hard cutoff at 10 mins.
celery_long: celery -A mysite worker -Q long_running -l info --time-limit=600 --soft-time-limit=540 -Ofair --autoscale=2,4 -n Long@%n


# celery workers for realtime stat updates from the trigger
celeryrt: celery -A mysite worker -Q realtime -l info --soft-time-limit=5 --autoscale=2,4 -n Realtime@%n


# purger is also a normal celery worker.
# this worker always wipes out the brokers existing/pending tasks on startup.
# without startup purge, its possible we will have WAY too to consume initially.
# Note: if you don't know what this is, don't enable it.
purger: celery -A mysite worker -l info --purge -n Purger


# the mandatory (and the only) worker responsible for running dataden.
# no other worker should consume from the queue this worker consumes from
#
#   -q : quick startup flag (for restarting without re-parsing initialization feeds)
#   -apiSpeedDelta <integer> : +/- values will increase or decrease the parse interval
#
dataden: java -Xmx1024m -jar dataden/dataden.jar -k 20491e2a4feda595b7347708915b200b -q -apiSpeedDelta -15 -t 8


# use this to reset the schedule, or startup from scratch
dataden_init: java -Xmx1024m -jar dataden/dataden.jar -k 20491e2a4feda595b7347708915b200b -apiSpeedDelta -15 -t 8


# the mandatory (and the only) worker responsible for running dataden triggers
# on the mongo database. this task ensures data is being pushed from mongo to django/postgres.
# 1x Dyno sport triggers using mongolab.com --> M3 <-- instance
trigger_nba: python manage.py sport_trigger nba --settings=mysite.settings.production_mongolab_m3
trigger_nhl: python manage.py sport_trigger nhl --settings=mysite.settings.production_mongolab_m3
trigger_nfl: python manage.py sport_trigger nflo --settings=mysite.settings.production_mongolab_m3
trigger_mlb: python manage.py sport_trigger mlb --settings=mysite.settings.production_mongolab_m3

