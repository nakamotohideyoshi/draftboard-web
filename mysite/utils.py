from ast import literal_eval
from logging import getLogger

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django_redis import get_redis_connection

logger = getLogger('mysite.utils')


def get_redis_instance():
    return get_redis_connection("default")


class QuickCache(object):
    """
    uniquely caches objects if they have an
    identifier field and a unix timestamp.

    Redis cache is used by default

    usage:

        e = {'id': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'dd_updated__id': 1464841517401,
            'something to cache': 'asdfasdf'}
        from mysite.utils import QuickCache
        class Steve(QuickCache):
            name = 'Steve' # naming the cache will help more uniquely identify it at runtime
        Steve(e) # caches e if it has a 'dd_updated__id' timestamp field and an 'id' field !
        # steve = Steve(s) # same as previous line if you want to return the instance of the cache
        e = Steve().fetch(1464841517401, '22052ff7-c065-42ee-bc8f-c4691c50e624')

    """

    class BytesIsNoneException(Exception):
        pass

    name = 'QuickCache'
    timeout_seconds = 60 * 5

    extra_key = '--%s--'
    # key_prefix_pattern = name + '--%s--'            # ex: 'QuickCache--%s--'
    # scan_pattern = key_prefix_pattern + '*'         # ex: 'QuickCache--%s--*'
    # key_pattern = key_prefix_pattern + '%s'         # ex: 'QuickCache--%s--%s'

    field_id = 'id'
    field_timestamp = 'dd_updated__id'

    def __init__(self, data=None, stash_now=True, override_cache=None):
        # self.key_prefix_pattern = self.name + '--%s--'            # ex: 'QuickCache--%s--'
        self.key_prefix_pattern = self.name + self.extra_key
        self.scan_pattern = self.key_prefix_pattern + '*'  # ex: 'QuickCache--%s--*'
        self.key_pattern = self.key_prefix_pattern + '%s'  # ex: 'QuickCache--%s--%s'

        self.cache = override_cache
        if self.cache is None:
            # default: use django default cache
            # TODO fix this hack

            self.cache = get_redis_instance()

        # immediately cache it based on 'stash_now' bool
        if data is not None and stash_now is True:
            self.stash(data)

    def get_key(self, ts, gid):
        key = self.key_pattern % (ts, gid)
        return key

    def scan(self, ts):
        """ return the keys for objects matching the same cache and timestamp 'ts' """
        redis = get_redis_instance()

        keys = []
        pattern = self.scan_pattern % ts
        for k in redis.scan_iter(pattern):
            keys.append(k)
        return keys

    def add_to_cache_method(self, k, data):
        return self.cache.set(k, data, self.timeout_seconds)

    def bytes_2_dict(self, bytes_to_convert):
        if bytes_to_convert is None:
            err_msg = 'bytes_2_dict(): bytes is None!'
            raise self.BytesIsNoneException(err_msg)
        return literal_eval(bytes_to_convert.decode())

    @staticmethod
    def validate_stashable(data):
        if not isinstance(data, dict):
            err_msg = 'data must be an instance of dict'
            raise Exception(err_msg)

    def fetch(self, ts, gid):
        k = self.get_key(ts, gid)
        ret_val = None
        try:
            ret_val = self.bytes_2_dict(self.cache.get(k))
        except self.BytesIsNoneException:
            pass
        return ret_val

    def stash(self, data):
        self.validate_stashable(data)
        ts = data.get('dd_updated__id')
        gid = data.get(self.field_id)
        k = self.get_key(ts, gid)
        ret_val = self.add_to_cache_method(k, data)
        return ret_val


def format_currency(amount):
    """
    Add a leading '$' to an amount, and a '-' before that if it is negative.
    :param amount: int or string
    :return:
    """
    pretty_amount = str(amount)

    if amount < 0:
        pretty_amount = pretty_amount[:1] + "$" + pretty_amount[1:]
    else:
        pretty_amount = "$%s" % pretty_amount

    return pretty_amount


def send_email(
        subject,
        recipients,
        title,
        message,
        signature='<p>--<br>Draftboard Staff</p>',
        sender=settings.DEFAULT_FROM_EMAIL,
        headers=None
):
    # don't send emails locally unless you come in here and change it
    if settings.DOMAIN == 'localhost':
        logger.warning('Email would normally be sent, title was %s, would send to %s' % (
            title, str(recipients)))
        return

    logger.info('Sending email to %s. Title: %s' % (recipients, title))
    context = {
        'domain': settings.DOMAIN,
        'site_name': 'Draftboard',
        'protocol': 'https',
        'title': title,
        'message': message,
        'signature': signature
    }

    html_content = get_template('email/default.html').render(context)

    if headers:
        headers = {'X-MC-Tags': headers}

    msg = EmailMultiAlternatives(
        subject,
        message,
        sender,
        recipients,
        headers=headers
    )
    msg.attach_alternative(html_content, "text/html")

    message_send_count = msg.send()

    logger.info('%s email(s) sent.' % message_send_count)
