#
# testlink.py

import random
import time

from django.core.management.base import BaseCommand

import push.classes
from dataden.cache.caches import (
    RandomId,
)
from dataden.watcher import OpLogObjWrapper
from push.classes import (
    StatsDataDenPush,
    PbpDataDenPush,
)


class Command(BaseCommand):
    """
    test thing for manage.py
    """

    help = "test the multi queue object"

    object_id_field = '_id'
    object_common_id_field = 'id'  # objects will be linked on this field
    common_ids = ['a', 'b', 'c']

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('values', nargs='+', type=str)

    def get_random_common_id(self):
        return self.common_ids[random.randint(0, len(self.common_ids) - 1)]

    def next_obj_id(self):
        self.obj_idx += 1
        return str(self.obj_idx)

    def next_test_obj(self, object_id=None, common_id=None):
        """
        using an incrementing unique object id mapped to '_id'
        and a random common linking id from self.common_ids,
        get the next test object to add

        :return:
        """

        oid = object_id
        if oid is None:
            oid = self.next_obj_id()

        cid = common_id
        if cid is None:
            cid = self.get_random_common_id()

        obj = {
            self.object_id_field: oid,
            self.object_common_id_field: cid,

            # different every run, easier to discern differences when obj debug printed
            'data': RandomId().get_random_id(),
        }
        livestats_obj = OpLogObjWrapper('test-sport', 'test-db', obj)
        return livestats_obj

    def __print_then_sleep(self, msg=None, sleep=None):

        time_to_sleep = sleep
        if time_to_sleep is None:
            time_to_sleep = 1

        message = msg
        if message is None:
            sleep_seconds_txt = '(%.1f sec sleep)' % float(sleep)
            message = '--------------------%s-------------------' % (sleep_seconds_txt)
        self.stdout.write(message)
        self.stdout.write('')
        self.stdout.write('')
        time.sleep(sleep)

    def handle(self, *args, **options):
        """
        generate a test game with questions

        :param args:
        :param options:
        :return:
        """
        self.obj_idx = 0  # set to initial value
        values = []
        for x in options['values']:
            values.append(x)

        default_sleep_seconds = 10

        # two of the same types of stats -- wont be linked, each sent out after delay expires
        obj1 = self.next_test_obj()
        obj2 = self.next_test_obj()
        StatsDataDenPush(push.classes.PUSHER_NBA_STATS, 'player').send(obj1)
        StatsDataDenPush(push.classes.PUSHER_NBA_STATS, 'player').send(obj2)
        self.__print_then_sleep(sleep=default_sleep_seconds)

        # two linked stats -- should be sent out immediately, as one thing! the delayed task wont send!
        #
        # IMPORTANT - we need to add the pbp objects to the "SENT" cache
        #             even if they are sent in a LINKED chunk of data
        obj3a = self.next_test_obj(common_id=self.common_ids[0])
        obj3b = self.next_test_obj(common_id=self.common_ids[0])
        PbpDataDenPush(push.classes.PUSHER_NBA_PBP, 'event').send(obj3a)
        StatsDataDenPush(push.classes.PUSHER_NBA_STATS, 'player').send(obj3b)
        self.__print_then_sleep(sleep=default_sleep_seconds)

        # # two linked stats -- the nba_stats sent first, the pbp second
        # #
        # # IMPORTANT - we need to add the pbp objects to the "SENT" cache
        # #             even if they are sent in a LINKED chunk of data
        # obj4a = self.next_test_obj(common_id=self.common_ids[1])
        # obj4b = self.next_test_obj(common_id=self.common_ids[1])
        # StatsDataDenPush( push.classes.PUSHER_NBA_STATS, 'player' ).send( obj4a )
        # PbpDataDenPush( push.classes.PUSHER_NBA_PBP, 'event' ).send( obj4b )
        # self.__print_then_sleep(sleep=default_sleep_seconds)
        #
        # # try resending the pbp -- it shouldnt be sent again!
        # # uses obj4b -- which was used previously
        # PbpDataDenPush( push.classes.PUSHER_NBA_PBP, 'event' ).send( obj4b )
        # # self.__print_then_sleep(sleep=6)
