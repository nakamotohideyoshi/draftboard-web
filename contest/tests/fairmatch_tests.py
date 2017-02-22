import unittest
from logging import getLogger

from contest.classes import (
    FairMatch
)

logger = getLogger('contest.test.fairmatch_test')


class FairMatchTest(unittest.TestCase):
    """
    unit tests (no database required) for contest.classes.FairMatch
    """

    @staticmethod
    def get_matched_entry_count(fm):
        # count the number of entries that are nested into their own lists.
        matched_entry_count = sum(len(x) for x in fm.contests['contests'])
        forced_entry_count = sum(len(x) for x in fm.contests['contests_forced'])
        # Add up # of contests created * contest size in order to find the # of matched entries.
        return forced_entry_count + matched_entry_count

    def get_accounted_for_entry_count(self, fm):
        # Get ALL entries, both match and unmatched.
        return self.get_matched_entry_count(fm) + len(fm.contests['unused_entries'])

    # Some basic sanity checks.
    def basic_contest_tests(self, fm, test_entries, contest_size):
        # make sure entry count is the same
        self.assertEqual(fm.contests['entry_pool_size'], len(test_entries))
        # make sure contest size is the same
        self.assertEqual(fm.contests['contest_size'], contest_size)
        # Make sure all entries were either matched or unmatched.
        self.assertEqual(self.get_accounted_for_entry_count(fm), len(test_entries))

    def test_single_entry(self):
        test_entries = [1]
        contest_size = 2
        fm = FairMatch(test_entries, contest_size, 'test_id')
        fm.run()
        self.basic_contest_tests(fm, test_entries, contest_size)

        # Did all entries either get matched or unmatched?
        self.assertEqual(self.get_accounted_for_entry_count(fm), len(test_entries))
        self.assertEqual(fm.contests['unused_entries'], [])

    def test_simple_h2h_contest_1(self):
        test_entries = [1, 1, 2, 3, 4, 5, 5, 5, 6, 7, 8, 9, 9, 9, 9, 9, 9, 9]
        contest_size = 2
        fm = FairMatch(test_entries, contest_size, 'test_id')
        fm.run()
        self.basic_contest_tests(fm, test_entries, contest_size)

        # Did all entries either get matched or unmatched?
        self.assertEqual(self.get_accounted_for_entry_count(fm), len(test_entries))
        # 9's 4-6 entries should never match because they are the only user with more th an 3
        # entries
        self.assertEqual(fm.contests['unused_entries'], [9, 9, 9, 9])

    def test_simple_h2h_contest_2(self):
        test_entries = [1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 6, 7, 8, 9]
        contest_size = 2
        fm = FairMatch(test_entries, contest_size)
        fm.run()
        self.basic_contest_tests(fm, test_entries, contest_size)

        # Did all entries either get matched or unmatched?
        self.assertEqual(self.get_accounted_for_entry_count(fm), len(test_entries))
        # There should only be 1 entry left out  of this contest pool configuration.
        self.assertEqual(len(fm.contests['unused_entries']), 1)

    def test_simple_h2h_contest_1_superlay(self):
        # In this situation there is only 1 entry, which means it must get a contest even if there
        # is nothing to match it against.
        test_entries = [1]
        contest_size = 2
        fm = FairMatch(test_entries, contest_size)
        fm.run()
        self.basic_contest_tests(fm, test_entries, contest_size)

        # In a Superlay contest, there are not enough entries to match into a contest, but a user
        # still has an unmatched 1st roudn entry, so they get a contest created even if there is no
        # opponent
        self.assertEqual(len(fm.contests['unused_entries']), 0)
        self.assertEqual(len(fm.contests['contests_forced']), 1)
        self.assertEqual(len(fm.contests['contests']), 0)

    def test_simple_h2h_contest_2_superlay(self):
        # Here there are 3 entries, which means two will match, and the other 1st rounder will get
        # a contest matched by itself.
        test_entries = [1, 2, 3]
        contest_size = 2
        fm = FairMatch(test_entries, contest_size)
        fm.run()
        self.basic_contest_tests(fm, test_entries, contest_size)

        # In a Superlay contest, there are not enough entries to match into a contest, but a user
        # still has an unmatched 1st roudn entry, so they get a contest created even if there is no
        # opponent
        self.assertEqual(len(fm.contests['unused_entries']), 0)
        # This is the important part: one of the entries needs to be forced into it's own contest.
        self.assertEqual(len(fm.contests['contests_forced']), 1)
        self.assertEqual(len(fm.contests['contests']), 1)

    def test_simple_3man_contest_1(self):
        test_entries = [1, 2, 3]
        contest_size = 3
        fm = FairMatch(test_entries, contest_size)
        fm.run()
        self.basic_contest_tests(fm, test_entries, contest_size)

        # 3 entries, contest size of 3: should have 1 contest and nothing else.
        self.assertEqual(len(fm.contests['unused_entries']), 0)
        self.assertEqual(len(fm.contests['contests_forced']), 0)
        self.assertEqual(len(fm.contests['contests']), 1)

    def test_simple_3man_contest_2(self):
        #
        test_entries = [1, 2, 3, 9]
        contest_size = 3
        fm = FairMatch(test_entries, contest_size)
        fm.run()
        self.basic_contest_tests(fm, test_entries, contest_size)

        # 3 entries, contest size of 3: should have 1 contest and nothing else.
        self.assertEqual(len(fm.contests['unused_entries']), 0)
        self.assertEqual(len(fm.contests['contests_forced']), 1)
        self.assertEqual(len(fm.contests['contests']), 1)
