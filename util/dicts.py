#
# util/dicts.py

from functools import reduce
from collections import Counter

class DictTools:

    @staticmethod
    def combine(d1, d2):
        """
        values are merged and added together for matching keys.

        example usage:

            >>> d1 = {'a':234, 'b':1}
            >>> d2 = {'b':1, 'c':123}
            >>> d = DictTools.combine(d1, d2)
            >>> d
            Counter({'b': 2, 'c': 123, 'a': 234})
            >>>

        :param d1: the target dict
        :param d2: using the key-value pairs in d2, combine and add them to d1
        :param exclude: list of keys to ignore.
        :return: Counter object - you can easily cast it to a dict if you wish with dict( Counter() )
        """

        def update_in_place(a, b):
            a.update(b)
            return a

        return reduce(update_in_place, (Counter(d) for d in [d1, d2]))

    @staticmethod
    def subtract(d1, d2):
        """
        removes the entries in d2 from d1, and returns d1.

        the caller should make copies of d1 if they wish to preserve its original data

        :param d1:
        :param d2:
        :return:
        """

        for k in d2.keys():
            try:
                d1.pop(k)
            except KeyError:
                pass
        return d1