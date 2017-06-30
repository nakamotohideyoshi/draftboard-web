web: newrelic-admin run-program gunicorn --pythonpath mysite mysite.wsgi -b 0.0.0.0:$PORT --workers $GUNICORN_WORKERS --max-requests $GUNICORN_MAX_REQUESTS --timeout $GUNICORN_TIMEOUT


# Runs the celerybeat scheduled tasks that can be found in the Django admin panel.
celerybeat: celery -A mysite beat


# Standard celery worker.
celery: newrelic-admin run-program celery -A mysite worker -l info --autoscale=2,1 --time-limit=600 -n Standard@%n


# Long-running celery task queue for things like <sport>.cleanup_roster that take a while.
# soft time limit of 9 mins, hard cutoff at 10 mins.
celery_long: newrelic-admin run-program celery -A mysite worker -Q long_running -l info --time-limit=600 --soft-time-limit=540 -Ofair --autoscale=2,1 -n Long@%n

# This has a stupid long timeout (24hrs) and should ONLY be used for the replayer.tasks.play_replay task.
celery_time_machine: newrelic-admin run-program celery -A mysite worker -Q time_machine -l info --time-limit=86400 -Ofair -n TimeMachine@%n

# celery workers for realtime stat updates from the trigger
celeryrt: newrelic-admin run-program celery -A mysite worker -Q realtime -l info --soft-time-limit=5 --autoscale=2,1 -n Realtime@%n


# purger is also a normal celery worker.
# this worker always wipes out the brokers existing/pending tasks on startup.
# without startup purge, its possible we will have WAY too to consume initially.
# Note: if you don't know what this is, don't enable it.
purger: newrelic-admin run-program celery -A mysite worker -l info --purge -n Purger


# the mandatory (and the only) worker responsible for running dataden triggers
# on the mongo database. this task ensures data is being pushed from mongo to django/postgres.
# 1x Dyno sport triggers using mongolab.com --> M3 <-- instance
trigger_nba: newrelic-admin run-program python manage.py sport_trigger nba --settings=mysite.settings.production_mongolab_m3
trigger_nhl: newrelic-admin run-program python manage.py sport_trigger nhl --settings=mysite.settings.production_mongolab_m3
trigger_nfl: newrelic-admin run-program python manage.py sport_trigger nflo --settings=mysite.settings.production_mongolab_m3
trigger_mlb: newrelic-admin run-program python manage.py sport_trigger mlb --settings=mysite.settings.production_mongolab_m3

