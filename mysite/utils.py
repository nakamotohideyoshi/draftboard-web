#
# mysite/utils.py

import os
import urllib
from ast import literal_eval
from redis import Redis

def get_redis_instance():
    url = os.environ.get('REDISCLOUD_URL') # TODO get this env var from settings
    if url is None:
        return Redis()
    else:
        redis_url = urllib.parse.urlparse(os.environ.get('REDISCLOUD_URL')) # TODO get this env var from settings
        r = Redis(host=redis_url.hostname, port=redis_url.port, password=redis_url.password, db=0)
        return r

class QuickCache(object):
    """
    uniquely caches objects if they have an
    identifier field and a unix timestamp.

    Redis cache is used by default

    usage:

        e = {'id': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'dd_updated__id': 1464841517401, 'something to cache': 'asdfasdf'}
        from mysite.utils import QuickCache
        class Steve(QuickCache):
            name = 'Steve' # naming the cache will help more uniquely identify it at runtime
        Steve(e) # caches e if it has a 'dd_updated__id' timestamp field and an 'id' field !
        # steve = Steve(s) # same as previous line if you want to return the instance of the cache
        e = Steve().fetch(1464841517401, '22052ff7-c065-42ee-bc8f-c4691c50e624')

    """

    class BytesIsNoneException(Exception): pass

    name = 'QuickCache'
    timeout_seconds = 60 * 5

    extra_key = '--%s--'
    # key_prefix_pattern = name + '--%s--'            # ex: 'QuickCache--%s--'
    # scan_pattern = key_prefix_pattern + '*'         # ex: 'QuickCache--%s--*'
    # key_pattern = key_prefix_pattern + '%s'         # ex: 'QuickCache--%s--%s'

    field_id = 'id'
    field_timestamp = 'dd_updated__id'

    def __init__(self, data=None, stash_now=True, override_cache=None):
        #self.key_prefix_pattern = self.name + '--%s--'            # ex: 'QuickCache--%s--'
        self.key_prefix_pattern = self.name + self.extra_key
        self.scan_pattern = self.key_prefix_pattern + '*'         # ex: 'QuickCache--%s--*'
        self.key_pattern = self.key_prefix_pattern + '%s'         # ex: 'QuickCache--%s--%s'

        self.cache = override_cache
        if self.cache is None:
            # default: use django default cache
            # TODO fix this hack

            self.cache = get_redis_instance()

        # immediately cache it based on 'stash_now' bool
        if data is not None and stash_now == True:
            self.stash(data)

    def get_key(self, ts, gid):
        key = self.key_pattern % (ts, gid)
        return key

    def scan(self, ts):
        """ return the keys for objects matching the same cache and timestamp 'ts' """

        #redis = Redis()
        redis = get_redis_instance()

        keys = []
        pattern = self.scan_pattern % ts
        #print('scan pattern:', pattern)
        for k in redis.scan_iter(pattern):
            keys.append(k)
        return keys

    def add_to_cache_method(self, k, data):
        return self.cache.set(k, data, self.timeout_seconds)

    def bytes_2_dict(self, bytes):
        if bytes is None:
            err_msg = 'bytes_2_dict(): bytes is None!'
            raise self.BytesIsNoneException(err_msg)
        return literal_eval(bytes.decode())

    def validate_stashable(self, data):
        if not isinstance(data, dict):
            err_msg = 'data must be an instance of dict'
            raise Exception(err_msg)

    #@timeit
    def fetch(self, ts, gid):
        k = self.get_key(ts, gid)
        ret_val = None
        #print('<<< fetch key: %s' % k)
        try:
            ret_val = self.bytes_2_dict(self.cache.get(k))
        except self.BytesIsNoneException:
            pass
        return ret_val

    #@timeit
    def stash(self, data):
        #
        self.validate_stashable(data)

        #
        ts = data.get('dd_updated__id')
        gid = data.get('id')
        k = self.get_key(ts, gid)
        #print('>>> stash key: %s' % k)
        #
        ret_val = self.add_to_cache_method(k, data)
        #print('stashed: key', str(k), ':', str(data))
        return ret_val