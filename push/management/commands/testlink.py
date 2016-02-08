#
# testlink.py

import random
from django.core.management.base import BaseCommand, NoArgsCommand
from dataden.cache.caches import (
    RandomId,
)
import push.classes
from push.classes import (
    DataDenPush,
    PbpDataDenPush,
)

class Command(BaseCommand):
    """
    test thing for manage.py
    """

    help = "test the multi queue object"

    object_id_field         = '_id'
    object_common_id_field  = 'common_id'
    common_ids              = ['a', 'b', 'c']

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('values', nargs='+', type=str)

    def get_random_common_id(self):
        return self.common_ids[ random.randint(0, len(self.common_ids) - 1)]

    def next_obj_id(self):
        self.obj_idx += 1
        return str(self.obj_idx)

    def next_test_obj(self):
        """
        using an incrementing unique object id mapped to '_id'
        and a random common linking id from self.common_ids,
        get the next test object to add

        :return:
        """
        obj = {
            self.object_id_field        : self.next_obj_id(),
            self.object_common_id_field : self.get_random_common_id(),

            # different every run, easier to discern differences when obj debug printed
            'data'                      : RandomId().get_random_id(),
        }
        return obj

    def handle(self, *args, **options):
        """
        generate a test game with questions

        :param args:
        :param options:
        :return:
        """
        self.obj_idx = 0 # set to initial value
        values = []
        for x in options['values']:
            values.append( x )

        #
        # create a fake stats object and send it with pusher (potentially delaying linking)

        # # two of the same types of stats -- wont be linked, each sent out after delay expires
        # DataDenPush( push.classes.PUSHER_NBA_STATS, 'player' ).send( self.next_test_obj(), async=True, force=False )
        # DataDenPush( push.classes.PUSHER_NBA_STATS, 'player' ).send( self.next_test_obj(), async=True, force=False )

        # two linked stats -- should be sent out immediately, as one thing! the delayed task wont send!
        obj = self.next_test_obj()
        DataDenPush( push.classes.PUSHER_NBA_STATS, 'player' ).send( obj, async=True, force=False )
        PbpDataDenPush( push.classes.PUSHER_NBA_PBP, 'event' ).send( obj, async=True, force=False )


