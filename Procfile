web: newrelic-admin run-program gunicorn --pythonpath mysite mysite.wsgi -b 0.0.0.0:$PORT --workers $GUNICORN_WORKERS --max-requests $GUNICORN_MAX_REQUESTS --timeout $GUNICORN_TIMEOUT

#
# runs the celerybeat scheduled tasks from the CELERYBEAT_SCHEDULE
# which should be found in mysite.celery_app.py
celerybeat: celery -A mysite beat -S djcelery.schedulers.DatabaseScheduler
#celerybeat: celery -A mysite beat -S celery.beat.PersistentScheduler

#
# the celery flag:  "-l info"   is required so that sumologic can parse tasks

#
# a worker for misc, very short-lived tasks (ie: milliseconds, hopefully).
#celery: celery -A mysite worker -l info -n celery1.%h
celery: celery -A mysite worker -l info            

# respawn after X tasks, w/ autoscaler
celery2: celery -A mysite worker -l info --maxtasksperchild=10 --autoscale=2,8

# another - if eacher worker spawns a celeryd, we dont need many of them thats for sure
celery3: celery -A mysite worker -l info --time-limit=600 --soft-time-limit=20 --maxtasksperchild=10

# another test
celery4: celery -A mysite worker -l info --time-limit=600 --soft-time-limit=20 --maxtasksperchild=10 --autoscale=1,2

# another test
celery5: celery -A mysite worker -l info -c 256 -P eventlet --time-limit=600 --soft-time-limit=20 --maxtasksperchild=10

#
# purger is also a normal celery worker.
# this worker always wipes out the brokers existing/pending tasks on startup.
# without startup purge, its possible we will have WAY too to consume initially.
purger: celery -A mysite worker -l info --purge

#
# the mandatory (and the only) worker responsible for running dataden.
# no other worker should consume from the queue this worker consumes from
#
#   -q : quick startup flag (for restarting without re-parsing initialization feeds)
#   -apiSpeedDelta <integer> : +/- values will increase or decrease the parse interval
#
dataden: java -Xmx1024m -jar dataden/dataden.jar -k 20491e2a4feda595b7347708915b200b -q -apiSpeedDelta -15 -t 8

# use this to reset the schedule, or startup from scratch
dataden_init: java -Xmx1024m -jar dataden/dataden.jar -k 20491e2a4feda595b7347708915b200b -apiSpeedDelta -15 -t 8

#
# the mandatory (and the only) worker responsible for running dataden triggers
# on the mongo database. this task ensures data is being pushed from mongo to django/postgres.
# 1x Dyno sport triggers using mongolab.com --> M3 <-- instance
trigger_nba: python manage.py sport_trigger nba --settings=mysite.settings.production_mongolab_m3
trigger_nhl: python manage.py sport_trigger nhl --settings=mysite.settings.production_mongolab_m3
trigger_nfl: python manage.py sport_trigger nfl --settings=mysite.settings.production_mongolab_m3
trigger_mlb: python manage.py sport_trigger mlb --settings=mysite.settings.production_mongolab_m3

