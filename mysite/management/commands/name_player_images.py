from django.conf import settings
from django.core.management.base import BaseCommand
from os import path
import re


class Command(BaseCommand):
    # example `python manage.py name_player_images <IMAGES_FOLDER> <SPORT>
    help = "Convert image filenames to player srids"

    def handle(self, *args, **options):
        def run_conversion(dirname, sport):
          original_dir = (path.join(settings.SITE_ROOT, 'player-photos/orig/%s/' % (dirname)),)
          dest_dir = (path.join(settings.SITE_ROOT, 'player-photos/dest/%s/' % (dirname)),)

          Player = __import__('sports.%s.models' % sport)

          # Team = __import__('sports.%s.models' % sport)
          # print(Team.objects.all())

          i = 0
          for team_folder in [x for x in original_dir.iterdir() if x.is_dir()]:
            team_name = team_folder.name.split(' ', 1)[-1]

            # # team updates
            # if team_name == 'OKC':
            #   team_name = 'Oklahoma City'

            for photo in team_folder.glob('*.png'):
              filename = re.split("\W+|_|-|\d+", photo.name)

              # print(filename)

              # last name, team, first name
              player = Player.objects.filter(last_name__icontains=filename[0])

              if player.count() > 1:
                player = player.filter(team__name__icontains=team_name)

              if player.count() > 1:
                player = player.filter(first_name__icontains=filename[1])

              # last name, first name, team
              player = Player.objects.filter(last_name__icontains=filename[0])

              if player.count() > 1:
                player = player.filter(first_name__icontains=filename[1])

              if player.count() > 1:
                player = player.filter(team__name__icontains=team_name)


              # first 4 chars of last name, team, first name
              if player.count() == 0:
                player = Player.objects.filter(last_name__icontains=filename[0][0:4])

                if player.count() > 1:
                  player = player.filter(team__name__icontains=team_name)

                if player.count() > 1:
                  player = player.filter(first_name__icontains=filename[1])


              # first 4 chars of last name, first name, team
              if player.count() == 0:
                player = Player.objects.filter(last_name__icontains=filename[0][0:4])

                if player.count() > 1:
                  player = player.filter(first_name__icontains=filename[1])

                if player.count() > 1:
                  player = player.filter(team__name__icontains=team_name)


              # see if last name was second word
              if player.count() == 0:
                player = Player.objects.filter(last_name__icontains=filename[1])

                if player.count() > 1:
                  player = player.filter(team__name__icontains=team_name)

                if player.count() > 1:
                  player = player.filter(first_name__icontains=filename[0])


              # last name is first 4 chars of second word
              if player.count() == 0:
                player = Player.objects.filter(last_name__icontains=filename[1][0:4])

                if player.count() > 1:
                  player = player.filter(team__name__icontains=team_name)

                if player.count() > 1:
                  player = player.filter(first_name__icontains=filename[0])


              # try first name as first word
              if player.count() == 0:
                player = Player.objects.filter(first_name__icontains=filename[0][0:4])

                if player.count() > 1:
                  player = player.filter(team__name__icontains=team_name)

                if player.count() > 1:
                  player = player.filter(last_name__icontains=filename[1])


              if player.count() == 1:
                  player = player[0]
                  photo.rename('%s/%s.png' % (dest_dir, player.srid))

              else:
                  print(team_folder.name, photo.name)
                  i += 1

          print('Total missing %s' % i)

        if len(args) == 2:
            # first arg is folder location, second arg is sport
            run_conversion(args[0], args[1])
        else:
            print('You must pass in the folder name')
