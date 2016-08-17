from __future__ import absolute_import

#
# tasks.py

from django.core.cache import cache
from mysite.celery_app import app

# TODO tasks to perform the parsing of injury updates for sport(s)