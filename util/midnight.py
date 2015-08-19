#
# util/midnight.py

from datetime import datetime, timedelta
from util.utctime import UtcTime

class Midnight(UtcTime):

    @staticmethod
    def get_midnight( dt ):
        """
        Get the first instant of the following day, with the
        same tzinfo of the object passed in.

        For the given datetime object 'dt', return midnight of that day,
        as in, time(0,0) of the following day.

        'tzinfo' parameter defaults to pytz.timezone('UTC')
        """

        tomorrow = dt + timedelta(hours=24)
        return datetime( tomorrow.year, tomorrow.month, tomorrow.day,
                                        0, 0, 0, 0, tzinfo=dt.tzinfo )

midnight = Midnight.get_midnight
