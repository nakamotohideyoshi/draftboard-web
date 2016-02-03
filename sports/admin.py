#
# sports/admin.py

from django.contrib import admin
import sports.models
import sports.classes
import mysite.mixins.generic_search
import django.db.utils

@admin.register(sports.models.SiteSport)
class SiteSport(admin.ModelAdmin):
    list_display = ['name','current_season']

class PlayerAdmin(admin.ModelAdmin):
    """
    inherited by sub module sports like nfl, nba, mlb, nhl
    """
    list_display    = ['srid','team','position','first_name','last_name']

    list_filter     = ['first_name','last_name','team','position']
    search_fields   = ['srid','first_name','last_name','position__name']

# class PlayerStatsAdmin(admin.ModelAdmin):
#     """
#     lists to be inherited by the actual sports
#     """
#
#     list_filter     = ['first_name','last_name']
#     search_fields   = ['first_name','last_name']

class PlayerStatsAdmin(mysite.mixins.generic_search.GenericSearchMixin, admin.ModelAdmin):

    #model           = Salary
    #list_filter     = ['first_name', 'flagged', 'pool']
    search_fields   = ('player__first_name', 'player__last_name')

    # def has_add_permission(self, request):
    #     return False

    try:
        related_search_mapping = {
            'player': {
                'content_type'  : 'player_type',
                'object_id'     : 'player_id',
                'ctypes'        : sports.classes.SiteSportManager().get_player_classes()
            }
        }
    except django.db.utils.ProgrammingError:
        # relation "django_content_type" does not exist
        print('relation "django_content_type" does not exist - this should only happen on the first migrate!')
