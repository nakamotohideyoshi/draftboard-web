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


class FairMatch(object):
    class ZeroEntriesException(Exception):
        pass

    class NotEnoughEntriesException(Exception):
        pass

    def __init__(self, entries=[],
                 contest_size=2):  # size / prize_structure will come from ContestPool instance
        # instance of random number generator
        self.r = Random()

        # size of contests to generate (ie: 10-mans)
        self.contest_size = contest_size

        # make a copy of original list of all the entries
        self.original_entries = list(entries)
        counter = Counter()
        for entry in self.original_entries:
            counter[entry] += 1
        self.counter_original_entries = counter

        # setup a Counter which will keep track of the runtime count of entries
        self.counter_runtime_entries = None

        # for debugging - a list of all the contests made
        self.contests = None

    def fill_contest(self, entries, force=False):
        """
        :param force: if force is true, skip the size check, and add the entries to contest regardless
        :return: list of the values that were used, otherwise raises
        """
        if len(entries) == 0:
            err_msg = 'Exception fill_contest() - 0 entries'
            raise self.ZeroEntriesException(err_msg)

        if not force and len(entries) < self.contest_size:
            err_msg = 'Exception fill_contest() - contest_size: %s, entries: %s' % (
                self.contest_size, str(entries))
            raise self.NotEnoughEntriesException(err_msg)

        ss = ''
        if force:
            ss = '** = superlay is possible here.'
        print('    making contest:', str(sorted(entries)), 'force:', str(force), '%s' % ss)

        self.__add_contest_debug(entries, self.contest_size, force=force)

        # counter will help us validate results along the way
        # primarily a debug thing.
        for e in entries:
            self.counter_runtime_entries[e] += 1

        # return a list of the entries used to create this contest
        return list(entries)

    def __add_contest_debug(self, entries, size, force=False):
        if force:
            # entries we need to enter into a contest no matter what (first entries)
            self.contests['contests_forced'].append(entries)
        else:
            # this
            self.contests['contests'].append(entries)
        self.contests['contest_size'] = size

    @staticmethod
    def lsubtract(l1, l2):
        """
        subtract the values in l2 from l1 and return the resulting list

        # todo raise exception if we cant remove an element?

        :param l1:
        :param l2:
        :return:
        """
        l = list(l1)  # copy l1 so we dont side effect it
        for x in l2:
            try:
                l.remove(x)
            except ValueError:
                print('    <!> couldnt remove entry: %s' % str(x))
        return l

    def run(self, verbose=True):
        """
        create all required contests using the FairMatch algorithm
        with the given user entries.
        """

        # initialize
        self.counter_runtime_entries = Counter()

        self.contests = {
            'entry_pool_size': len(list(self.original_entries)),
            'entry_pool': list(self.original_entries),
            'contests': [],
            'contests_forced': []
        }

        # run the algorithm. give it a copy of the total entries
        self.run_h(1, list(self.original_entries), exclude=[], verbose=True)

    def run_h(self, round, entries, exclude=[], verbose=True):
        """
        run FairMatch starting with the specified round and entries, plus optional excludes

        :param round: integer # of the round
        :param entries: total pool of entries. remove entries only if they've been filled into a contest.
        :param exclude: entries from the previous round that got 2 fills
        :param verbose: more output when True
        """

        # the list of unique entries to select from
        uniques = list(set(entries) - set(exclude))
        n_uniques = len(uniques)

        if n_uniques < self.contest_size:
            self.contests['unused_entries'] = entries
            self.contests['FairMatch_unused_uniques'] = uniques
            self.contests['FairMatch_unused_unq_cnt'] = n_uniques
            print('done! unique entries: %s < contest size: %s   '
                  '-> so we cant make anymore contests' % (n_uniques, self.contest_size))
            return

        # additional 2nd entries this round. includes duplicates (potentially),
        # because we havent yet selected uniques.
        additional = list(set(self.lsubtract(entries, uniques)))

        if verbose:
            print('')
            print('+++ round %s +++' % str(round))
            print('entries:', str(sorted(entries)), '   (%s total)' % str(len(entries)))
            print('uniques:', str(sorted(uniques)), '   (%s total)' % str(len(uniques)))
            print('additional:', str(sorted(additional)), '   (%s total)' % str(len(additional)))
            print('exclude:', str(sorted(exclude)), '   (%s total)' % str(len(exclude)))

        while True:
            # 0. randomize the order of the values in the lists we will take from
            shuffle(uniques)
            shuffle(additional)
            shuffle(exclude)

            # 1. fill contests using values from uniques, until we cant.
            try:
                used_entries = self.fill_contest(uniques[:self.contest_size])
                entries = self.lsubtract(entries, used_entries)
                uniques = self.lsubtract(uniques, used_entries)
            except (self.NotEnoughEntriesException, self.ZeroEntriesException) as e:
                print('        ', str(e))
                break

        # the number of extra entries we would need to completely fill a contest
        n = self.contest_size - len(uniques)

        # 2. if we have enough additional values, use them.
        #    here we know we have to use all uniques, so
        #    be sure to remove duplicate values from exclude first!
        additional = list(set(additional) - set(uniques))
        shuffle(additional)
        chosen_additional = additional[:n]
        possible_excludes = []
        if round == 1:
            used_entries = self.fill_contest(uniques + chosen_additional, force=True)
            # contest filled, now remove the values from entries (and update additional)
            # entries = self.lsubtract(entries, used_entries)
            # update additional in case we use later, though that is unlikely
            # additional = self.lsubtract(additional, chosen_additional)

        # 3. round >= 2. (ie: dealing with 2nd+ entries)
        else:
            chosen_entries = uniques + chosen_additional
            n = self.contest_size - len(chosen_entries)
            if n < 0:
                raise Exception('too many contest entries in Round %s step' % str(round))

            elif n == 0:
                # we have the right amount -- fill a contest
                # used_entries = self.fill_contest(chosen_entries, force=False)
                # entries = self.lsubtract(entries, chosen_entries)
                # # update remaining
                pass  # it will all work when this falls outside this elif block

            else:  # ie: n > 0
                # grab values from the excludes as a last resort.
                # be sure to remove duplicates already in the chosen ones
                possible_excludes = list(set(exclude) - set(chosen_entries))
                shuffle(possible_excludes)
                chosen_entries.extend(possible_excludes[:n])

            # it could fail here still, but lets run it and see what happens
            try:
                used_entries = self.fill_contest(chosen_entries, force=False)
            except self.NotEnoughEntriesException as e:
                # it may not be possible to make this.
                # stash un-filled entries in the 'unused_entries' contests data
                print(' >>>>>> entries into next round: %s' % str(entries))
                return self.run_h(round + 1, entries, exclude=[], verbose=verbose)

        entries = self.lsubtract(entries, used_entries)

        # recursive call handles the next round
        existing_excludes = []
        for exclude_entry in chosen_additional:
            if exclude_entry in entries:
                existing_excludes.append(exclude_entry)

        print(
            '+++ and round %s >>> entries %s <<<  and > excludes %s <  ]]] existing_excludes: %s [[['
            'heading into round [%s]' % (str(round), str(entries),
                                         str(chosen_additional), str(existing_excludes),
                                         str(round + 1)))

        self.run_h(round + 1, entries, exclude=existing_excludes, verbose=verbose)

    def print_debug_info(self):
        # # remove the forced contest entries from the leftover 'unused_entries'
        # unused_entries = list(self.contests['unused_entries'])
        # for contest in self.contests['contests_forced']:
        #     for entry in contest:
        #         unused_entries.remove(entry)
        # # now update the actual unused entries
        # self.contests['unused_entries'] = unused_entries

        #
        print('*** %s *** post run() information ***' % self.__class__.__name__)
        # print(self.contests)
        for k, v in self.contests.items():
            if k == 'entry_pool':
                continue
            print('%-16s:' % k, v)

        count_total_entries = 0
        counter = Counter()
        for contest in self.contests['contests']:
            for entry in contest:
                counter[entry] += 1
                count_total_entries += 1
        for contest in self.contests['contests_forced']:
            for entry in contest:
                counter[entry] += 1
                count_total_entries += 1
        for entry in self.contests['unused_entries']:
            counter[entry] += 1

        standard = len(self.contests['contests'])
        forced = len(self.contests['contests_forced'])
        total = standard + forced

        # print('original entries (before):', str(sorted(dict(self.counter_original_entries).items())))
        # print('counter entries (after)  :', str(sorted(dict(counter).items())))
        orig = dict(self.counter_original_entries).copy()
        after = dict(counter)

        print('%s original entries, %s final entries in contests + %s in '
              'unused_entries' % (str(len(self.original_entries)),
                                  str(count_total_entries),
                                  str(len(self.contests['unused_entries']))))
        print('%s total contests (%s standard, %s forced)' % (total, standard, forced))
        if orig != after:
            print(
                '(debug) orig != after   ->   this indicates we lost/added a rando entry somewhere. very bad.')
            print('orig : %s' % str(orig))
            print('')
            print('after: %s' % str(after))


class FairMatchNoCancel(FairMatch):
    """
    extends FairMatch to guarantee all lineups get filled into contests.
    """

    unused_entries = 'unused_entries'
    contests_no_cancel = 'contests_no_cancel'

    def run(self):
        """
        specifically at the end of the original FairMatch, places
        all unused entries into contests. this will, of course,
        never place a lineup for the same user into any contest more than one time.
        """

        # run the original FairMatch algorithm
        super().run()

        # intialize the extra list of contests
        self.contests[self.contests_no_cancel] = []
        contests = []

        # fill contests with the remaining unused lineups leftover from original run
        entries = self.contests[self.unused_entries]

        while entries != []:
            uniques = list(set(entries))
            used_entries = self.fill_contest(uniques, force=True)
            contests.append(used_entries)
            entries = self.lsubtract(entries, used_entries)
            self.contests[self.unused_entries] = entries  # set the remaining entries

        # set the FairMatchNoCancel contests we just created
        self.contests[self.contests_no_cancel] = contests

    def print_debug_info(self):
        super().print_debug_info()
        no_cancel_contests = len(self.contests[self.contests_no_cancel])
        print('%s additional "NoCancel" contests' % no_cancel_contests)
