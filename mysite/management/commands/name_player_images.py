from django.core.management.base import NoArgsCommand
from pathlib import Path
from sports.nba.models import Player
import re


class Command(NoArgsCommand):
    help = "Wipe django's default cache."

    def handle_noargs(self, **options):
        i = 0
        # This is much better and works on redis.
        base_folder = Path('./static/original-photos/380height/')

        for team_folder in [x for x in base_folder.iterdir() if x.is_dir()]:
          team_city = team_folder.name.split(' ', 1)[0]

          if team_city == 'OKC':
            team_city = 'Oklahoma City'

          for photo in team_folder.glob('*.png'):
            filename = re.split("\W+|_|-", photo.name)

            # if len(filename) == 4:
            #   filename = re.split("\w+(?:-\w+)+|_|\.|,", photo.name)
              # print('FOURRRRR', photo.name, filename, filename2)

            # last name, team, first name
            player = Player.objects.filter(last_name__icontains=filename[0])

            if player.count() > 1:
              player = player.filter(team__market__icontains=team_city)

            if player.count() > 1:
              player = player.filter(first_name__icontains=filename[1])


            # last name, first name, team
            player = Player.objects.filter(last_name__icontains=filename[0])

            if player.count() > 1:
              player = player.filter(first_name__icontains=filename[1])

            if player.count() > 1:
              player = player.filter(team__market__icontains=team_city)


            # first 4 chars of last name, team, first name
            if player.count() == 0:
              player = Player.objects.filter(last_name__icontains=filename[0][0:4])

              if player.count() > 1:
                player = player.filter(team__market__icontains=team_city)

              if player.count() > 1:
                player = player.filter(first_name__icontains=filename[1])


            # first 4 chars of last name, first name, team
            if player.count() == 0:
              player = Player.objects.filter(last_name__icontains=filename[0][0:4])

              if player.count() > 1:
                player = player.filter(first_name__icontains=filename[1])

              if player.count() > 1:
                player = player.filter(team__market__icontains=team_city)


            # see if last name was second word
            if player.count() == 0:
              player = Player.objects.filter(last_name__icontains=filename[1])

              if player.count() > 1:
                player = player.filter(team__market__icontains=team_city)

              if player.count() > 1:
                player = player.filter(first_name__icontains=filename[0])


            # last name is first 4 chars of second word
            if player.count() == 0:
              player = Player.objects.filter(last_name__icontains=filename[1][0:4])

              if player.count() > 1:
                player = player.filter(team__market__icontains=team_city)

              if player.count() > 1:
                player = player.filter(first_name__icontains=filename[0])


            # try first name as first word
            if player.count() == 0:
              player = Player.objects.filter(first_name__icontains=filename[0][0:4])

              if player.count() > 1:
                player = player.filter(team__market__icontains=team_city)

              if player.count() > 1:
                player = player.filter(last_name__icontains=filename[1])


            if player.count() == 1:
                player = player[0]
                photo.rename('./static/player-photos/380/%s.png' % (player.srid))

            else:
                print(team_folder.name, photo.name,)
                i += 1

        print('Total %s' % i)