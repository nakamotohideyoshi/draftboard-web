#
# fairmatch.py

from random import Random, shuffle

class FairMatch(object):

    class ZeroEntriesException(Exception): pass

    class NotEnoughEntriesException(Exception): pass

    def __init__(self, entries=[], contest_size=2):  # size / prize_structure will come from ContestPool instance
        # instance of random number generator
        self.r = Random()

        # size of contests to generate (ie: 10-mans)
        self.contest_size = contest_size

        # make a copy of original list of all the entries
        self.original_entries = list(entries)

        # for debugging - a list of all the contests made
        self.contests = None

    def get_contests(self):
        """
        :return: a list of lists-of-entries to fill contests
        """
        return self.contests['contests']

    def get_contests_forced(self):
        """
        :return: a list of lists-of-unfilled-entries, ie the superlay contest entries
        """
        return self.contests['contests_forced']

    def fill_contest(self, entries, size, force=False):
        """
        :param force: if force is true, skip the size check, and add the entries to contest regardless
        :return:
        """
        if len(entries) == 0:
            err_msg = '0 entries passed to fill_contest()'
            raise self.ZeroEntriesException(err_msg)

        if not force and len(entries) < size:
            err_msg = '%s needed, entries list: %s' % (size, str(entries))
            raise self.NotEnoughEntriesException(err_msg)

        ss = ''
        if force:
            ss = '** = superlay is possible here.'
        print('    making contest:', str(entries), 'force:', str(force), '%s'%ss)
        # TODO fill c

        self.__add_contest_debug(entries, size, force=force)

    def __add_contest_debug(self, entries, size, force=False):
        if force:
            # entries we need to enter into a contest no matter what (first entries)
            self.contests['contests_forced'].append( entries )
        else:
            # this
            self.contests['contests'].append( entries )
        self.contests['contest_size'] = size

    def run(self):
        """
        create all required contests using the FairMatch algorithm
        with the given user entries.
        """

        self.contests = {
            'entry_pool_size'   : len(list(self.original_entries)),
            'entry_pool'        : list(self.original_entries),
            'contests'          : [],
            'contests_forced'   : []
        }

        # run the algorithm, starting it all off by passing
        # a mutable copy of all the unique entries to run_h()
        all_entries = list(self.original_entries)
        self.run_h(all_entries, 1, [], verbose=True)

        # now set the unused entries
        unused_entries = self.contests['entry_pool']
        for c in self.contests['contests']:
            for entry in c:
                unused_entries.remove(entry)
        self.contests['unused_entries'] = unused_entries

        # cleanup. dont leave contests_forced entries in the unused_entries
        # remove the forced contest entries from the leftover 'unused_entries'
        unused_entries = list(self.contests['unused_entries'])
        for contest in self.contests['contests_forced']:
            for entry in contest:
                unused_entries.remove(entry)
        # now update the actual unused entries
        self.contests['unused_entries'] = unused_entries

    def get_and_remove_uniques(self, entries, exclude):
        """
        breaks up the list of entries into two lists:
         a) all unique entries
         b) the remaining pool of entries after 1 of each unique has been removed

        :param entries: all entries pool
        :param exclude: ignore these entries
        :return: a tuple of two lists in the form: (unique_entries, remaining_entries)
        """
        uniques = list(set(entries) - set(exclude))
        for e in uniques:
            entries.remove(e)
        # also remove the excludes! they might not have been
        # entirely removed because uniques will not
        return uniques, entries

    def remove_from_list(self, target, removes):
        for e in removes:
            target.remove(e)
        return target

    def get_additional_uniques(self, entries, n, exclude):
        """
        get 'n' uniques out of 'entries', excluding those in 'exclude' list

        removes the entries return from the original 'entries' list

        :param entries:
        :param n:
        :param exclude:
        :return:
        """

        additional_uniques = list(set(entries))
        print('        get %sx entry from %s ignoring entries in %s' % (str(n), str(additional_uniques), str(exclude)))
        # excludes the entries we already have
        for e in exclude:
            try:
                additional_uniques.remove(e)
            except ValueError:
                pass # e didnt exist
        shuffle(additional_uniques)
        additional_uniques = additional_uniques[:n]

        entries = self.remove_from_list(entries, additional_uniques)

        return additional_uniques, entries

    def run_h(self, entries, round, exclude, verbose=False):
        """
        check for any priority entries from the previous round
        and get them into contests if possible.

        continue onto the main contest generation loop,
        and fill all the entries at this round that we can.

        :param remaining_uniques: all first entries for this round
        :param round: integer number of the round starting with 1
        :param priority: entries with priority (from previous round)
        :return:
        """
        if entries == [] and exclude == []:
            if verbose:
                print('done!')
            return # we are done

        if verbose:
            print('')
            print('++++ beginning of round %s ++++' % str(round))
            print('(pre-round) entry pool:', str(entries), '   (%s total)'%str(len(entries)))

        # get the unique entries for this round
        round_uniques, remaining_entries = self.get_and_remove_uniques(entries, exclude)
        remaining_uniques = list(set(remaining_entries) - set(exclude))
        if verbose:
            print('excluded(for fairness):', str(sorted(exclude)))
            print('round uniques         :', str(sorted(round_uniques)), '   (%s total)' % str(len(round_uniques)))
            print('remaining entries     :', str(sorted(remaining_entries)), 'including any entries in exclude (debug)')
            print('remaining uniques     :', str(sorted(remaining_uniques)), 'not including excludes. potential additional entries this round')

        #exclude_users_for_fairness = []
        unchosen_second_entries = []
        selected_additional_entries = []
        while True:
            # shuffle the entries and then select enough for a contest
            shuffle(round_uniques)
            random_contest_entries = round_uniques[:self.contest_size]

            try:
                # create and fill a contest using the random entries
                self.fill_contest(random_contest_entries, self.contest_size)
                # remove entries from the round uniques once they are filled
                round_uniques = self.remove_from_list(round_uniques, random_contest_entries)

            except self.ZeroEntriesException:
                break

            except self.NotEnoughEntriesException:
                # attempt to fill one last contest by randomly
                # selecting additional entries from the remaining pool of uniques.
                # in order to be fair, add additional selected users to a
                # list of excludes to prevent them from getting fills
                # next round (because they would have had 2 fills this round).
                n = self.contest_size - len(round_uniques)
                # get n additional uniques from the remaining uniques, not including
                # whatever is currently in round_uniques
                additional_uniques = list(set(remaining_uniques) - set(round_uniques))
                shuffle(additional_uniques)
                selected_additional_entries = additional_uniques[:n]

                if verbose:
                    print('        -> %s didnt get filled.' % str(round_uniques))
                    # print('        -> selected_additional_entries = '
                    #       'list(set(remaining_uniques) - set(round_uniques))[:n]')    # # # # #
                    print('        -> randomly chose:', str(selected_additional_entries), 'from', str(additional_uniques), ''
                                        '(avoiding these obviously:', str(round_uniques),')')

                # now make the last contest of the round, or issue refunds
                first_round = round == 1
                try:
                    self.fill_contest(round_uniques + selected_additional_entries, self.contest_size, force=first_round)
                except:
                    # failed on the last time around, but there may be enough
                    # excludes required to create the last contest on
                    # one more round so break and try again

                    break

                # these must be added back to the entries pool for next round
                unchosen_second_entries = list(set(additional_uniques) - set(selected_additional_entries))
                # be sure to remove successfully filled entries from the total remaining entries
                entries = self.remove_from_list(entries, selected_additional_entries)
                break

        if verbose: print('    (exclude %s in round %s)' % (str(selected_additional_entries),str(round+1)))

        # we must add the 'additional_uniques' back to the entries!
        # although earlier there was a chance they would get 2 fills in a round,
        # 'additional_uniques' are the entries that did not -- so back to the pool they go
        self.run_h(entries + unchosen_second_entries, round+1, selected_additional_entries, verbose=verbose)

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
        for k,v in self.contests.items():
            if k == 'entry_pool':
                continue
            print('%-16s:'%k, v)

        standard = len(self.contests['contests'])
        forced = len(self.contests['contests_forced'])
        total = standard + forced
        print('%s total contests (%s standard, %s forced)' % (total, standard, forced))

class FairMatchNoCancel(FairMatch):
    """
    extends FairMatch to guarantee all lineups get filled into contests.
    """

    unused_entries      = 'unused_entries'
    contests_no_cancel  = 'contests_no_cancel'

    def run(self):
        """
        specifically at the end of the original FairMatch, places
        all unused entries into contests. this will, of course,
        never place a lineup for the same user into any contest more than one time.
        """

        # run the original FairMatch algorithm
        super().run()

        # fill contests with the remaining unused lineups leftover from original run
        remaining_entries = self.contests[self.unused_entries]

        # intialize the extra list of contests
        self.contests[self.contests_no_cancel] = []

        entries = list(remaining_entries) # copy
        while entries != []:
            contest_entries, entries = self.get_additional_uniques(entries, self.contest_size, [])
            self.contests[self.contests_no_cancel].append(contest_entries)

            # unused_entries = self.contests[self.unused_entries]
            # for entry in contest_entries:
            #     unused_entries
            self.contests[self.unused_entries] = entries # set the remaining entries

    def print_debug_info(self):
        super().print_debug_info()
        no_cancel_contests = len(self.contests['contests_no_cancel'])
        print('%s additional "NoCancel" contests' % no_cancel_contests)