from django.utils import timezone
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from sports.classes import SiteSportManager
from contest.models import LobbyContestPool


class Command(BaseCommand):
    """
    This sends upcoming games and contest to the site admin.

    Usage:

        $> ./manage.py send_upcoming_issues <sport>                                 # single sport
        $> ./manage.py send_upcoming_issues <sport1> <sport2> ... <sport4>          # you can list all sports

    """

    # help is a Command inner variable
    help = 'usage: ./manage.py updatecontent <sport>'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('sport', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        generate an email with upcoming games and contest

        :param args:
        :param options:
        :return:
        """

        msg = 'getting upcoming games and contests'
        self.stdout.write( msg )

        sitesport_mng = SiteSportManager()
        data = {}
        for sport in options['sport']:
            upcoming = sitesport_mng.get_scoreboard_games(sport)
            contests = LobbyContestPool.objects.select_related(
                'site_sport', 'draft_group', 'prize_structure'
            ).prefetch_related('prize_structure__ranks', 'prize_structure__generator').filter(site_sport__name=sport)
            data[sport] = {'games': upcoming, 'contests': contests}

        subject = 'Upcoming issues'
        ctx = {
            'data': data
        }

        message = render_to_string('emails/upcoming_games.html', ctx)

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])


