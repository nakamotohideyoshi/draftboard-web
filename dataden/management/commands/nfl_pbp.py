#
# replayer/management/commands/playupdate.py

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from replayer.classes import ReplayManager
from dataden.watcher import (
    OpLogObjWrapper,
)
from sports.nfl.parser import (
    PbpEventParser,
)

class Command(BaseCommand):
    """
    given an NFLO play srid, show the raw data, along with situation (location/possession objects)

    srids are SportRadar global ids that look like this:
        556b318a-f944-4b37-86dd-4b0dba4d0644

    any string after the playSrid will cause the command
    to try to package and send the play like a realtime stat!
    """
    USAGE_STR   = './manage.py nfl_pbp <playSrid> [<optional send flag>]'

    # help is a Command inner variable
    help = 'usage: ' + USAGE_STR

    parser = None

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('srids', nargs='+', type=str)

    def handle(self, *args, **options):
        i = 0
        play_srid = None
        words = []
        send = False
        for arg in options['srids']:
            if i == 0:
                play_srid = arg
            if i == 1:
                send = True
            words.append(arg)
            i += 1

        phrase = ' '.join(words)

        self.stdout.write('+++ nflo play objects | %s +++' % play_srid)
        self.stdout.write('-------------------------------------------------------')
        #self.stdout.write('description must contain:     "%s"' % str(phrase))
        self.stdout.write('')

        from dataden.classes import DataDen
        dd = DataDen()

        db = 'nflo'
        parent_api = 'pbp'

        # get the play object
        play = None
        target = {
            'id': play_srid,
            # 'description': {
            #     '$regex': phrase
            # }
        }
        plays = dd.find(db, 'play', parent_api, target=target)
        for obj in plays:
            play = obj

        # play_srid = play.get('id')
        #play_srid = srid # because were passing it into the command now

        sl = None  # start location object
        sp = None  # start possession object
        el = None  # end location object
        ep = None  # end possession object

        # start situation data
        situation_list_id = 'start_situation__list'
        situation = play.get(situation_list_id, {})

        sl_srid = situation.get('location', '')
        locations = dd.find(db, 'location', parent_api,
                            {'id': sl_srid, 'play__id': play_srid, 'parent_list__id': situation_list_id})
        for obj in locations:
            sl = obj

        sp_srid = situation.get('possession', '')
        possessions = dd.find(db, 'possession', parent_api,
                              {'id': sp_srid, 'play__id': play_srid, 'parent_list__id': situation_list_id})
        for obj in possessions:
            sp = obj

        # end situation data
        situation_list_id = 'end_situation__list'
        situation = play.get(situation_list_id, {})

        el_srid = situation.get('location', '')
        locations = dd.find(db, 'location', parent_api,
                            {'id': el_srid, 'play__id': play_srid, 'parent_list__id': situation_list_id})
        for obj in locations:
            el = obj

        ep_srid = situation.get('possession', '')
        possessions = dd.find(db, 'possession', parent_api,
                              {'id': ep_srid, 'play__id': play_srid, 'parent_list__id': situation_list_id})
        for obj in possessions:
            ep = obj

        sport_db = 'nflo'
        parent_api = 'pbp'
        self.stdout.write("sport_db = '%s'" % sport_db)
        self.stdout.write("parent_api = '%s'" % parent_api)
        self.stdout.write('')

        self.print_obj('start_location', sl, 'location', sport_db=sport_db, parent_api=parent_api, send=send)
        self.print_obj('start_possession', sp, 'possession', sport_db=sport_db, parent_api=parent_api, send=send)
        self.print_obj('end_location', el, 'location', sport_db=sport_db, parent_api=parent_api, send=send)
        self.print_obj('end_possession', ep, 'possession', sport_db=sport_db, parent_api=parent_api, send=send)
        self.print_obj('play', play, 'play', sport_db=sport_db, parent_api=parent_api, send=send)

        self.stdout.write('') # one more space at the end of output

    def print_obj(self, name, data, coll, sport_db=None, parent_api=None, send=False):
        self.stdout.write('')
        self.stdout.write('%s = %s' % (name, str(data)))
        self.stdout.write("self.__parse_and_send(%s, (sport_db + '.' + '%s', parent_api))" % (name, coll))
        if send == True:
            if sport_db is None:
                raise Exception('sport_db is None! if you are trying to send the play it must exist... ')
            if parent_api is None:
                raise Exception('parent_api is None! if you are trying to send the play it must exist... ')
            # sport_db = 'nflo'
            # parent_api = 'pbp'
            # start_location = {'parent_list__id': 'start_situation__list', 'id': '97354895-8c77-4fd4-a860-32e62ea7382a',
            #                   'game__id': 'acbb3001-6bb6-41ce-9e91-942abd284e4c', 'market': 'New England',
            #                   'reference': 4960.0, 'quarter__id': '8075b247-bb26-4f49-a342-968f04835d2d',
            #                   'dd_updated__id': 1464842199562, 'alias': 'NE', 'name': 'Patriots',
            #                   'play__id': 'da1dbdf1-b501-48dd-a728-72b9d8f31ec8',
            #                   '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGFjYmIzMDAxLTZiYjYtNDFjZS05ZTkxLTk0MmFiZDI4NGU0Y3F1YXJ0ZXJfX2lkODA3NWIyNDctYmIyNi00ZjQ5LWEzNDItOTY4ZjA0ODM1ZDJkcGFyZW50X2xpc3RfX2lkc3RhcnRfc2l0dWF0aW9uX19saXN0ZHJpdmVfX2lkMjFkZGViN2QtMTNmYS00YjgxLWJiMWYtZDA4MDQ4NDFlMDk3cGxheV9faWRkYTFkYmRmMS1iNTAxLTQ4ZGQtYTcyOC03MmI5ZDhmMzFlYzhpZDk3MzU0ODk1LThjNzctNGZkNC1hODYwLTMyZTYyZWE3MzgyYQ==',
            #                   'yardline': 35.0, 'parent_api__id': 'pbp',
            #                   'drive__id': '21ddeb7d-13fa-4b81-bb1f-d0804841e097'}
            # self.__parse_and_send(start_location, (sport_db + '.' + 'location', parent_api))

            # build the namespace (ns) # ie: 'nfl.play' or 'nfl.location', etc...
            ns = '%s.%s' % (sport_db, coll)
            self.parse_and_send(data, (ns, parent_api))


    def parse_and_send(self, unwrapped_obj, target, tag=None):
        # create a new parser instance
        self.parser = PbpEventParser()

        #
        parts = target[0].split('.')
        oplog_obj = OpLogObjWrapper(parts[0], parts[1], unwrapped_obj)
        if tag is not None:
            print('tag:', tag)

        self.parser.parse(oplog_obj, target=target)
