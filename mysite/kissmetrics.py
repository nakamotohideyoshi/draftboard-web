import KISSmetrics
from django.conf import settings


def get_kissmetrics():
    return KISSmetrics.Client(key=settings.KISS_ANALYTICS_CODE)


def track_contest_end(username, data):
    KM = get_kissmetrics()
    KM.record(username, 'Contest Finished', data)