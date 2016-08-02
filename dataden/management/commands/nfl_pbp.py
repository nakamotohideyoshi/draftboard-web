#
# replayer/management/commands/playupdate.py

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from replayer.classes import ReplayManager

class Command(BaseCommand):
    """
    given an NFLO play srid, show the raw data, along with situation (location/possession objects)

    srids are SportRadar global ids that look like this: 556b318a-f944-4b37-86dd-4b0dba4d0644
    """
    USAGE_STR   = './manage.py nfl_pbp <play srid>'

    # help is a Command inner variable
    help = 'usage: ' + USAGE_STR

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('srids', nargs='+', type=str)

    def handle(self, *args, **options):
        i = 0
        play_srid = None
        words = []
        for arg in options['srids']:
            if i == 0:
                play_srid = arg
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
        self.print_obj('start_location', sl, 'location')
        self.print_obj('start_possession', sp, 'possession')
        self.print_obj('end_location', el, 'location')
        self.print_obj('end_possession', ep, 'possession')
        self.print_obj('play', play, 'play')
        self.stdout.write('') # one more space at the end of output

    def print_obj(self, name, data, coll):
        self.stdout.write('')
        self.stdout.write('%s = %s' % (name, str(data)))
        self.stdout.write("self.__parse_and_send(%s, (sport_db + '.' + '%s', parent_api))" % (name, coll))