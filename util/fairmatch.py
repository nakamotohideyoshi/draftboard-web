#
# fairmatch.py

from collections import Counter
from functools import reduce
from random import Random, shuffle


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


#
# class FairMatchNoCancel(FairMatch):
#     """
#     extends FairMatch to guarantee all lineups get filled into contests.
#     """
#
#     unused_entries = 'unused_entries'
#     contests_no_cancel = 'contests_no_cancel'
#
#     def run(self):
#         """
#         specifically at the end of the original FairMatch, places
#         all unused entries into contests. this will, of course,
#         never place a lineup for the same user into any contest more than one time.
#         """
#
#         # run the original FairMatch algorithm
#         super().run()
#
#         # intialize the extra list of contests
#         self.contests[self.contests_no_cancel] = []
#         contests = []
#
#         # fill contests with the remaining unused lineups leftover from original run
#         entries = self.contests[self.unused_entries]
#
#         while entries != []:
#             uniques = list(set(entries))
#             used_entries = self.fill_contest(uniques, force=True)
#             contests.append(used_entries)
#             entries = self.lsubtract(entries, used_entries)
#             self.contests[self.unused_entries] = entries  # set the remaining entries
#
#         # set the FairMatchNoCancel contests we just created
#         self.contests[self.contests_no_cancel] = contests
#
#     def print_debug_info(self):
#         super().print_debug_info()
#         no_cancel_contests = len(self.contests[self.contests_no_cancel])
#         print('%s additional "NoCancel" contests' % no_cancel_contests)
