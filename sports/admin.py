from django.contrib import admin

import sports.classes
import sports.models
import mysite.mixins.generic_search
import django.db.utils


# @admin.register(sports.models.PlayerStats)
# class PlayerStatsAdmin(mysite.mixins.generic_search.GenericSearchMixin, admin.ModelAdmin):
#
#     list_display = ['player','amount','flagged','pool', 'primary_roster', 'fppg']
#     list_editable = ['amount', 'flagged']
#     model = sports.models.PlayerStats
#     list_filter = [ 'primary_roster', 'flagged', 'pool']
#     raw_id_admin = ('pool', )
#     search_fields = ('player__first_name', 'player__last_name')
#     def has_add_permission(self, request):
#         return False
#
#     try:
#         related_search_mapping = {
#             'player': {
#                 'content_type':'player_type',
#                 'object_id': 'player_id',
#                 'ctypes': sports.classes.SiteSportManager().get_player_classes()
#             }
#         }
#     except django.db.utils.ProgrammingError:
#         # relation "django_content_type" does not exist
#         print('relation "django_content_type" does not exist - this should only happen on the first migrate!')

class PlayerAdmin(admin.ModelAdmin):
    """
    inherited by sub module sports like nfl, nba, mlb, nhl
    """
    list_display = ['srid','team','position','first_name','last_name']
