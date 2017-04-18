#
# dataden/management/commands/qtest.py

import random

from django.core.management.base import BaseCommand

from dataden.cache.caches import (
    RandomId,
    LinkedExpiringObjectQueueTable,
)


class Command(BaseCommand):
    """
    test thing for manage.py
    """

    help = "test the multi queue object"

    object_id_field = '_id'
    object_common_id_field = 'common_id'
    common_ids = ['a', 'b', 'c']

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('values', nargs='+', type=str)

    def get_random_common_id(self):
        return self.common_ids[random.randint(0, len(self.common_ids) - 1)]

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
            self.object_id_field: self.next_obj_id(),
            self.object_common_id_field: self.get_random_common_id(),

            # different every run, easier to discern differences when obj debug printed
            'data': RandomId().get_random_id(),
        }
        return obj

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

        #
        # create our custom queue instance using the names in the array
        qt = LinkedExpiringObjectQueueTable(values)

        # add 1 random object to each queue in the QueueTable
        # for i in range(len(values)):
        #     mq.add( values[i], self.next_test_obj() )
        #     mq.add( values[i], self.next_test_obj() )

        qt.add(values[0], self.next_test_obj())
