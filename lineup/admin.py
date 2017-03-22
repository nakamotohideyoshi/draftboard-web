from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from lineup.models import Lineup


class LineupAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'created', 'updated', 'fantasy_points', 'draft_group', 'sport']
    readonly_fields = ('user', 'fantasy_points', 'draft_group', 'lineup_players',)
    list_filter = ['created', 'updated']

    @staticmethod
    def lineup_players(obj):
        player_display = mark_safe("<ul>")

        if obj.draft_group.fantasy_points_finalized is None:
            return "Cannot view the players in a lineup until it's contest is finished."

        for player in obj.players.all():
            player_display += format_html(
                "<li>"
                "<strong>Roster Spot:</strong> {}<br />"
                "<strong>sport.models.player:</strong> {}<br />    "
                "<strong>draftgroup.models.player:</strong> {} <br /><br />"
                "</li>",
                player.roster_spot,
                "%s" % player.player,
                "%s" % player.draft_group_player
            )

        player_display += mark_safe("</ul>")
        return player_display


admin.site.register(Lineup, LineupAdmin)
