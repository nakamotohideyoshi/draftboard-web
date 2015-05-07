#
# keyprefix/classes.py

import keyprefix.models

class UsesCacheKeyPrefix(object):
    """
    all caches should implement this class.

    a site admin/developer can look at the KeyPrefix objects in the db
    before picking a name for their object which add to cache.

    its a way of getting the various objects which add to the cache
    to do so with a certain prefix, but without being able to enforce
    that, its more of a simple way to get child classes to
    simply update the prefix they ARE using and have it viewable
    in the admin.
    """

    def __init__(self):
        self.my_prefix = self.__class__.__name__
        try:
            k = keyprefix.models.KeyPrefix.objects.get(prefix=self.my_prefix)
        except keyprefix.models.KeyPrefix.DoesNotExist:
            k = keyprefix.models.KeyPrefix()
            k.prefix = self.my_prefix
            k.save()

    def get_key_prefix_only(self):
        return self.my_prefix

    def get_key(self, hsh):
        return '%s%s' % (self.get_key_prefix_only(), hsh)