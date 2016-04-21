web: newrelic-admin run-program gunicorn --pythonpath mysite mysite.wsgi -b 0.0.0.0:$PORT --workers $GUNICORN_WORKERS --max-requests $GUNICORN_MAX_REQUESTS --timeout $GUNICORN_TIMEOUT

#
# runs the celerybeat scheduled tasks from the CELERYBEAT_SCHEDULE
# which should be found in mysite.celery_app.py
celerybeat: celery -A mysite beat -S djcelery.schedulers.DatabaseScheduler
#celerybeat: celery -A mysite beat -S celery.beat.PersistentScheduler

#
# a worker for misc, very short-lived tasks (ie: milliseconds, hopefully).
#
# this worker always wipes out the brokers existing/pending tasks on startup.
# without startup purge, its possible we will have WAY too to consume initially.
celery: celery -A mysite worker -l info -n celery1.%h

purger: celery -A mysite worker -l info -n celery1.%h --purge

#
# the mandatory (and the only) worker responsible for running dataden.
# no other worker should consume from the queue this worker consumes from
#
#   -q : quick startup flag (for restarting without re-parsing initialization feeds)
#   -apiSpeedDelta <integer> : +/- values will increase or decrease the parse interval
#
dataden: java -jar dataden/dataden.jar -k 20491e2a4feda595b7347708915b200b -q -apiSpeedDelta -15 -t 8

#
# the mandatory (and the only) worker responsible for running dataden triggers
# on the mongo database. this task ensures data is being pushed from mongo to django/postgres.
# no other worker should consume from the this worker consumes from
#dataden_trigger: celery -A mysite worker -l info -c 1 -Q q_dataden_trigger
#dataden_trigger: celery -A mysite worker -c 1 -l info -Q q_dataden_trigger -n dataden_trigger1.%h

#
# non-celery way of running dataden triggers on the mongo database
#dataden_trigger: python manage.py dataden_trigger

trigger_nba: python manage.py sport_trigger nba
trigger_nhl: python manage.py sport_trigger nhl
trigger_nfl: python manage.py sport_trigger nfl
trigger_mlb: python manage.py sport_trigger mlb

#
######################################################################################################
# For SumoLogic, make these triggers have the dyno name
# in the Process name, so we can filter on it.
#
# *Warning*
#   Only ONE trigger per sport should run at a time!
#
#
# Notes:
#   mongolab_m1: a mongolab.com M1 multi-node instance (primary+ replica set. ~1.5gb ram, 40gb ssd)
#   mongolab_m3: a mongolab.com M3 single-node instance (primary node, ~7.5gb ram, ~100gb ssd)
#
######################################################################################################

#
# 1x, 2x, Performance-M, Performance-L sport triggers using mongolab.com --> M1 <-- instance
trigger_nba_1x_m1: python manage.py sport_trigger nba --settings=mysite.settings.production_mongolab_m1
trigger_nhl_1x_m1: python manage.py sport_trigger nhl --settings=mysite.settings.production_mongolab_m1
trigger_nfl_1x_m1: python manage.py sport_trigger nfl --settings=mysite.settings.production_mongolab_m1
trigger_mlb_1x_m1: python manage.py sport_trigger mlb --settings=mysite.settings.production_mongolab_m1

#trigger_nba_2x_m1: python manage.py sport_trigger nba --settings=mysite.settings.production_mongolab_m1
#trigger_nhl_2x_m1: python manage.py sport_trigger nhl --settings=mysite.settings.production_mongolab_m1
#trigger_nfl_2x_m1: python manage.py sport_trigger nfl --settings=mysite.settings.production_mongolab_m1
#trigger_mlb_2x_m1: python manage.py sport_trigger mlb --settings=mysite.settings.production_mongolab_m1
#
#trigger_nba_performanceM_m1: python manage.py sport_trigger nba --settings=mysite.settings.production_mongolab_m1
#trigger_nhl_performanceM_m1: python manage.py sport_trigger nhl --settings=mysite.settings.production_mongolab_m1
#trigger_nfl_performanceM_m1: python manage.py sport_trigger nfl --settings=mysite.settings.production_mongolab_m1
#trigger_mlb_performanceM_m1: python manage.py sport_trigger mlb --settings=mysite.settings.production_mongolab_m1
#
#trigger_nba_performanceL_m1: python manage.py sport_trigger nba --settings=mysite.settings.production_mongolab_m1
#trigger_nhl_performanceL_m1: python manage.py sport_trigger nhl --settings=mysite.settings.production_mongolab_m1
#trigger_nfl_performanceL_m1: python manage.py sport_trigger nfl --settings=mysite.settings.production_mongolab_m1
#trigger_mlb_performanceL_m1: python manage.py sport_trigger mlb --settings=mysite.settings.production_mongolab_m1

#
# 1x, 2x, Performance-M, Performance-L sport triggers using mongolab.com --> M3 <-- instance
trigger_nba_1x_m3: python manage.py sport_trigger nba --settings=mysite.settings.production_mongolab_m3
trigger_nhl_1x_m3: python manage.py sport_trigger nhl --settings=mysite.settings.production_mongolab_m3
trigger_nfl_1x_m3: python manage.py sport_trigger nfl --settings=mysite.settings.production_mongolab_m3
trigger_mlb_1x_m3: python manage.py sport_trigger mlb --settings=mysite.settings.production_mongolab_m3

#trigger_nba_2x_m3: python manage.py sport_trigger nba --settings=mysite.settings.production_mongolab_m3
#trigger_nhl_2x_m3: python manage.py sport_trigger nhl --settings=mysite.settings.production_mongolab_m3
#trigger_nfl_2x_m3: python manage.py sport_trigger nfl --settings=mysite.settings.production_mongolab_m3
#trigger_mlb_2x_m3: python manage.py sport_trigger mlb --settings=mysite.settings.production_mongolab_m3
#
#trigger_nba_performanceM_m3: python manage.py sport_trigger nba --settings=mysite.settings.production_mongolab_m3
#trigger_nhl_performanceM_m3: python manage.py sport_trigger nhl --settings=mysite.settings.production_mongolab_m3
#trigger_nfl_performanceM_m3: python manage.py sport_trigger nfl --settings=mysite.settings.production_mongolab_m3
#trigger_mlb_performanceM_m3: python manage.py sport_trigger mlb --settings=mysite.settings.production_mongolab_m3
#
#trigger_nba_performanceL_m3: python manage.py sport_trigger nba --settings=mysite.settings.production_mongolab_m3
#trigger_nhl_performanceL_m3: python manage.py sport_trigger nhl --settings=mysite.settings.production_mongolab_m3
#trigger_nfl_performanceL_m3: python manage.py sport_trigger nfl --settings=mysite.settings.production_mongolab_m3
#trigger_mlb_performanceL_m3: python manage.py sport_trigger mlb --settings=mysite.settings.production_mongolab_m3

#
# 1x, 2x, Performance-M, Performance-L sport triggers using mongolab.com --> ec2 (amazon) <-- instance
trigger_nba_1x_ec2: python manage.py sport_trigger nba --settings=mysite.settings.production_mongo_ec2
trigger_nhl_1x_ec2: python manage.py sport_trigger nhl --settings=mysite.settings.production_mongo_ec2
trigger_nfl_1x_ec2: python manage.py sport_trigger nfl --settings=mysite.settings.production_mongo_ec2
trigger_mlb_1x_ec2: python manage.py sport_trigger mlb --settings=mysite.settings.production_mongo_ec2

# 2x_ec2 procs
# performanceM_ec2 procs
# performanceL_ec2 procs

#
# dataden processes:
#   1) be sure to double-check/update their datadenapp.com settings! (connect to the proper mongo instance!)
#   2) use the uniquely named processes to differentiate processes in sumoLogic -- even though they run the same thing
dataden_1x_m1: java -jar dataden/dataden.jar -k 20491e2a4feda595b7347708915b200b -q -apiSpeedDelta -15 -t 8
#dataden_2x_m1: java -jar dataden/dataden.jar -k 20491e2a4feda595b7347708915b200b -q -apiSpeedDelta -15 -t 8
#dataden_performanceM_m1: java -jar dataden/dataden.jar -k 20491e2a4feda595b7347708915b200b -q -apiSpeedDelta -15 -t 8
#dataden_performanceL_m1: java -jar dataden/dataden.jar -k 20491e2a4feda595b7347708915b200b -q -apiSpeedDelta -15 -t 8

dataden_1x_m3: java -jar dataden/dataden.jar -k 20491e2a4feda595b7347708915b200b -q -apiSpeedDelta -15 -t 8
#dataden_2x_m3: java -jar dataden/dataden.jar -k 20491e2a4feda595b7347708915b200b -q -apiSpeedDelta -15 -t 8
#dataden_performanceM_m3: java -jar dataden/dataden.jar -k 20491e2a4feda595b7347708915b200b -q -apiSpeedDelta -15 -t 8
#dataden_performanceL_m3: java -jar dataden/dataden.jar -k 20491e2a4feda595b7347708915b200b -q -apiSpeedDelta -15 -t 8

dataden_1x_ec2: java -jar dataden/dataden.jar -k 20491e2a4feda595b7347708915b200b -q -apiSpeedDelta -15 -t 8
#dataden_2x_ec2: java -jar dataden/dataden.jar -k 20491e2a4feda595b7347708915b200b -q -apiSpeedDelta -15 -t 8
#dataden_performanceM_ec2: java -jar dataden/dataden.jar -k 20491e2a4feda595b7347708915b200b -q -apiSpeedDelta -15 -t 8
#dataden_performanceL_ec2: java -jar dataden/dataden.jar -k 20491e2a4feda595b7347708915b200b -q -apiSpeedDelta -15 -t 8

