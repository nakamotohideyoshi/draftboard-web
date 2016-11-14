from django.contrib import (
    admin,
    messages,
)
import statscom.models


@admin.register(statscom.models.PlayerLookup)
class PlayerLookupAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'player', 'created', 'updated', 'pid', ]
    list_filter = ['sport', 'created', 'updated', ]
    search_fields = ['first_name', 'last_name', 'pid']

    @staticmethod
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
        msg = '%s player lookup entries removed.' % (num_players)
        messages.success(request, msg)

    actions = [
        remove_selected_players,
    ]
