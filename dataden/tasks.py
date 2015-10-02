from __future__ import absolute_import

from mysite.celery_app import app
from .watcher import Trigger
from django.conf import settings
import subprocess

@app.task(bind=True)
def dataden(self):
    """
    run dataden jar via command line

    :return:
    """
    cmd_str = 'java -jar dataden/dataden-rio.jar -k %s' % settings.DATADEN_LICENSE_KEY
    command = cmd_str.split()
    popen = subprocess.Popen(command, stdout=subprocess.PIPE)
    lines_iterator = iter(popen.stdout.readline, b"")
    for line in lines_iterator:
        print(line) # yield line

@app.task(bind=True)
def dataden_trigger(self):
    """
    run dataden triggers on the mongo database

    :return:
    """
    trigger = Trigger()
    trigger.run()

@app.task
def test_dataden(pool):
    """

    :param pool:
    :return:
    """
    pass