web: newrelic-admin run-program gunicorn --pythonpath mysite mysite.wsgi -b 0.0.0.0:$PORT --workers $GUNICORN_WORKERS --max-requests $GUNICORN_MAX_REQUESTS --timeout $GUNICORN_TIMEOUT

#celery: python ./manage.py celeryd
#celery: celery -A mysite worker -l info
#worker: celery -A mysite worker -l info
worker: celery -A mysite worker -l info --autoscale=6,2

#celery: python ./manage.py celerybeat
celery: celery -A mysite beat -S djcelery.schedulers.DatabaseScheduler
