#
# dataden/util/simpletimer.py

import datetime
from django.utils import timezone

class SimpleTimer(object):

    def __init__(self):
        self.__started  = None
        self.__stopped  = None
        self.__sum      = None

    def start(self, clear_sum=False):
        if clear_sum:
            self.__sum = None
        self.__started  = timezone.now()

    def stop(self, print_now=True, msg='', sum=False):
        """
        returns a datetime.timedelta of the difference. (stop - start)

        :param print_now:
        :param msg:
        :return:
        """
        self.__stopped = timezone.now()
        if print_now:
            self.prnt(msg)
        td = self.__stopped - self.__started
        self.__add_to_sum( td )
        return td

    def prnt(self, msg=''):
        one_sec = datetime.timedelta(seconds=1)
        td_diff = self.__stopped - self.__started
        ms_str = ''
        if td_diff < one_sec:
            ms_str = '(%s ms)' % str( int(td_diff.microseconds / 1000 ) )
        print( td_diff, ms_str, msg )

    def __add_to_sum(self, td):
        if self.__sum is None:
            self.__sum = td
        else:
            self.__sum = self.__sum + td

    def get_sum(self):
        return self.__sum