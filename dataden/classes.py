#
# dataden/classes.py

import dataden.cache.caches

class DataDen(object):
    """
    caleb: im intending on this being the thru-point for rest_api calls
    """

    def __init__(self):
        #
        # get the default cache for DataDen
        self.live_stats_cache = dataden.cache.caches.LiveStatsCache()
