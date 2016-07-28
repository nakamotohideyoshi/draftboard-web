web: newrelic-admin run-program gunicorn --pythonpath mysite mysite.wsgi -b 0.0.0.0:$PORT --workers $GUNICORN_WORKERS --max-requests $GUNICORN_MAX_REQUESTS --timeout $GUNICORN_TIMEOUT

#
# runs the celerybeat scheduled tasks from the CELERYBEAT_SCHEDULE
# which should be found in mysite.celery_app.py
celerybeat: celery -A mysite beat -S djcelery.schedulers.DatabaseScheduler
#celerybeat: celery -A mysite beat -S celery.beat.PersistentScheduler

#
# a worker for misc, very short-lived tasks (ie: milliseconds, hopefully).
celery: celery -A mysite worker -l info -n celery1.%h

# respawn after X tasks, w/ autoscaler
celery2: celery -A mysite worker --maxtasksperchild=5000 --autoscale=4,16

#
# purger is also a normal celery worker.
# this worker always wipes out the brokers existing/pending tasks on startup.
# without startup purge, its possible we will have WAY too to consume initially.
purger: celery -A mysite worker -l info -n celery1.%h --purge

#
# the mandatory (and the only) worker responsible for running dataden.
# no other worker should consume from the queue this worker consumes from
#
#   -q : quick startup flag (for restarting without re-parsing initialization feeds)
#   -apiSpeedDelta <integer> : +/- values will increase or decrease the parse interval
#
dataden: java -Xmx1024m -jar dataden/dataden.jar -k 20491e2a4feda595b7347708915b200b -q -apiSpeedDelta -15 -t 8

#
# the mandatory (and the only) worker responsible for running dataden triggers
# on the mongo database. this task ensures data is being pushed from mongo to django/postgres.
# 1x Dyno sport triggers using mongolab.com --> M3 <-- instance
trigger_nba: python manage.py sport_trigger nba --settings=mysite.settings.production_mongolab_m3
trigger_nhl: python manage.py sport_trigger nhl --settings=mysite.settings.production_mongolab_m3
trigger_nfl: python manage.py sport_trigger nfl --settings=mysite.settings.production_mongolab_m3
trigger_mlb: python manage.py sport_trigger mlb --settings=mysite.settings.production_mongolab_m3

