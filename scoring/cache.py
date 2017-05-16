from django.core.cache import caches

from keyprefix.classes import UsesCacheKeyPrefix


class ScoreSystemCache(UsesCacheKeyPrefix):
    """
    Get the cache for the specified sport's scoring system stat values.
    """

    KEY = "score_system"
    TIMEOUT = 360

    def __init__(self, sport, name='default', clear=False, key_version=1):
        super().__init__()

        self.c = caches[name]  # 'default' is the settings.CACHES['default'] !
        if clear:
            self.clear()
        self.sport = sport
        self.key_version = key_version

    def clear(self):
        self.c.delete(self.__key())  # removes the item at the key
        self.stat_values = []

    def __key(self):
        """
        uses the sport, which is incorporated in the cache key
        :return:
        """
        return self.get_key(self.KEY + '_' + self.sport)

    def add_stat_values(self, stat_values):
        """
        Cache the stat_values.

        Returns whether the stats_values were added.
        Returns False if we tried to add them but they were already in the cache.

        :param stat_values:
        :return:
        """
        was_added = self.c.add(self.__key(), stat_values, self.TIMEOUT, version=self.key_version)
        return was_added

    def get_stat_values(self):
        """
        Does a cache hit to find the stat values, otherwise queries
        them from the database and stashes it in the cache.

        :return:
        """
        return self.c.get(self.__key(), None)
