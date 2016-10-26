#
# sports/admin.py

from django.contrib import admin
import sports.models
import sports.classes
import mysite.mixins.generic_search
import django.db.utils
import logging

logger = logging.getLogger('django')


@admin.register(sports.models.SiteSport)
class SiteSport(admin.ModelAdmin):
    list_display = ['name', 'current_season']


class PlayerAdmin(admin.ModelAdmin):
    """
    inherited by sub module sports like nfl, nba, mlb, nhl
    """
    list_display = ['first_name', 'last_name',
                    'on_active_roster', 'position', 'team', 'srid', 'status']

    list_filter = ['on_active_roster', 'position', 'last_name', 'first_name']
    search_fields = ['srid', 'first_name', 'last_name', 'position__name']


class PlayerLineupName(admin.ModelAdmin):

    list_display = ['first_name', 'last_name', 'lineup_nickname']
    list_filter = ['first_name', 'last_name', 'lineup_nickname']
    search_fields = ['first_name', 'last_name', 'position__name', 'lineup_nickname']
    list_editable = ['lineup_nickname']


class PlayerStatsAdmin(mysite.mixins.generic_search.GenericSearchMixin, admin.ModelAdmin):

    # model           = Salary
    # list_filter     = ['first_name', 'flagged', 'pool']
    search_fields = ('srid_game', 'srid_player', 'player__first_name', 'player__last_name')
    ordering = ['-created']
    # def has_add_permission(self, request):
    #     return False

    try:
        related_search_mapping = {
            'player': {
                'content_type': 'player_type',
                'object_id': 'player_id',
                'ctypes': sports.classes.SiteSportManager().get_player_classes()
            }
        }
    except django.db.utils.OperationalError:
        # relation "django_content_type" does not exist
        logger.error(
            """relation "django_content_type" does not exist - this should only happen on the first
            migrate!""")


class GameAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_filter = ['status', 'start', 'home', 'away']
    search_fields = ['status', 'start', 'srid']
