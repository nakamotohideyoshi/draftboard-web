#
# admin.py

from django.contrib import (
    admin,
    messages,
)
import statscom.models

@admin.register(statscom.models.PlayerLookup)
class PlayerLookupAdmin(admin.ModelAdmin):

    # we want it to show all of them, always
    list_max_show_all = 9999
    list_per_page = 9999

    list_display = ['created','updated','player','pid', 'first_name', 'last_name']
    list_filter = ['created','updated','pid']

    def remove_selected_players(self, request, queryset):
        """
        deletes the selected objects so the admin can cleanup this admin panel
        """
        num_players = queryset.count()
        if num_players == 0:
            messages.success(request, 'NO PLAYERS SELECTED - 0 players removed')
            return

        queryset.delete()

        # task finished. presumably salaries have been updated based on latest projections
        msg = '%s player lookup entries removed.' % (str(num_players))
        messages.success(request, msg)

    actions = [
        remove_selected_players,
    ]