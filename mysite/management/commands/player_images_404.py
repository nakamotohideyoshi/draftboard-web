from http import client

from django.core.management.base import BaseCommand

from sports.nba.models import Player


def get_status_code(host, path="/"):
    """ This function retreives the status code of a website by requesting
        HEAD data from the host. This means that it only requests the headers.
        If the host cannot be reached or something else goes wrong, it returns
        None instead.
    """
    try:
        conn = client.HTTPConnection(host)
        conn.request("HEAD", path)
        return conn.getresponse().status
    except Exception:
        return None


class Command(BaseCommand):
    help = "Wipe django's default cache."

    def handle(self, *args, **options):
        players = Player.objects.all()

        i = 0
        for player in players:
            i += 1

            if i % 100 == 0:
                print('Through %s' % i)

            player_image = '/nba/120/%s.png' % player.srid
            player_status = get_status_code('djh3pixt0wof0.cloudfront.net', player_image)

            if player_status in [403, 404]:
                print('%s, %s %s, %s' % (
                player.srid, player.first_name, player.last_name, player.team.name))
