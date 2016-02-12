#
# push/utils.py

from datetime import timedelta
from functools import reduce
import operator # for operator.and_  and operator.or_
from django.db.models import Q
from replayer.models import Update
from sports.classes import SiteSportManager
import re

class AbstractLinkerStats(object):

    update_class = Update

    def __init__(self, sport):
        self.sport = sport
        self.verbose = False
        self.debug_limit = 0
        self.pbp_parent_api = 'pbp'
        self.stats_parent_api = 'stats'
        self.delay_seconds = 5
        self.delay_seconds_behind = 0

        ssm = SiteSportManager()
        self.site_sport = ssm.get_site_sport(self.sport)
        self.player_class = ssm.get_player_class(self.site_sport)

    def run(self):
        raise Exception('inheriting classes must override this method')

class LinkerManager(AbstractLinkerStats):

    def __init__(self, sport):
        super().__init__(sport)

        self.player_srid_pattern = r"'player':\s'([^']*)'"
        self.pbp_player_scoring_related_parent_list_names = [
            'fieldgoal__list',
            'rebound__list',
            'turnover__list',
            'steal__list',
            'assist__list',
            #'personalfoul__list',      # not related to scoring
            'freethrow__list',
            #'attemptblocked__list',    # not related to scoring
            'block__list',
            #'technicalfoul__list',     # not related to scoring
            #'flagrantfoul__list',      # not related to scoring
            'statistics__list',
            #'ejection__list'           # not related to scoring
        ]

    def run(self, delay_deltas=(0,0), limit=None):
        """
        generate the statistics for the linker based on the settings

        :param delay_deltas: open the window for linking stats by (x,y) where we add x behind, and y ahead (seconds)
        :return:
        """
        total_delay_behind  = self.delay_seconds_behind + delay_deltas[0]
        total_delay         = self.delay_seconds + delay_deltas[1]

        players = self.player_class.objects.all()
        player_srids = [ p.srid for p in players ]
        #len(player_srids)
        q_player_srids = [ Q(o__icontains=srid) for srid in player_srids ]
        #len(q_player_srids)
        q_ns_contains_sport_prefix = Q(ns__icontains='%s.event'%self.sport)
        pbp_updates = self.update_class.objects.filter(Q(o__contains="'parent_api__id': '%s'" % self.pbp_parent_api),
                                                       q_ns_contains_sport_prefix )
        print( pbp_updates.count(), 'pbp_updates (total)')
        q_player_pbp_parent_lists = [ Q(o__icontains="'parent_list__id': '%s'"%parent_list) for parent_list in self.pbp_player_scoring_related_parent_list_names ]
        sub_pbp_updates = pbp_updates.filter(reduce(operator.or_, q_player_srids))
        print( sub_pbp_updates.count(), 'sub_pbp_updates (pbp players)')
        # only run on the sub_pbp_updates -- ie: the ones we care about related to scoring!
        pbp_updates = sub_pbp_updates

        #pbp_updates.count()
        stat_updates = self.update_class.objects.filter(Q(o__contains="'parent_api__id': '%s'" % self.stats_parent_api),
                                                        q_ns_contains_sport_prefix)
        #stat_updates.count()

        stats_map = {}
        i = 0
        ctr = 0
        for x in range(99):
            stats_map[x] = 0
        total_pbp_updates = pbp_updates.count()
        for pbp in pbp_updates:
            ctr += 1
            print('--------------------------- %s / %s ----------------------------' % (str(ctr), str(total_pbp_updates)))
            print('pbp >>>', str(pbp))
            player_srids = re.findall(self.player_srid_pattern, str(pbp))
            for psrid in player_srids:
                print('        >>>', psrid)
            dt_behind       = pbp.ts - timedelta(seconds=total_delay)
            dt_ahead        = pbp.ts + timedelta(seconds=total_delay_behind)
            linking_range   = (dt_behind, dt_ahead)
            linkable_stats  = stat_updates.filter( Q(ts__range=linking_range) & reduce(operator.or_, q_player_srids) )
            num_stats_linked = linkable_stats.count()
            stats_map[ num_stats_linked ] += 1
            print( num_stats_linked, 'linked')
            print('-----------------------------------------------------------------')
            print('')
            print('')
            if i >= self.debug_limit and self.debug_limit != 0:
                break
            i += 1

        f = open('nba_linkerstats_%s_%s.txt'%(total_delay_behind, total_delay),'w')
        #
        msg1 = '[%s]' % self.sport
        print(msg1)
        f.write(msg1 + '\n')
        #
        msg2 = 'window(sec) %s - %s' % (total_delay_behind, total_delay)
        print(msg2)
        f.write(msg2 + '\n')
        #
        x = stats_map
        summary = [ '%s linked: %s times'%(str(k),str(x[k])) for k in x.keys() if x[k] != 0 ]

        for s in summary:
            print( s )
            f.write(s + '\n')

        if f is not None:
            f.close()