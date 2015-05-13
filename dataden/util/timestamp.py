#
#

import datetime
from django.utils import timezone

class Parse(object):

    def from_string(s):
        """
        parse a timestamp from sportsradar feeds of the form: 2015-04-18T16:30:00+00:00

        :return:
        """

        DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
        dt_str = s.split('+')[0]
        dt = datetime.datetime.strptime( dt_str, DATETIME_FORMAT )
        int_val = int(dt.strftime('%s'))
        return datetime.datetime.fromtimestamp( int_val, tz=timezone.utc )

    from_string = staticmethod(from_string)