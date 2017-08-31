from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from lineup.models import Lineup
from sports.classes import SiteSportManager


class LineupAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'created', 'updated', 'fantasy_points', 'draft_group', 'sport']
    readonly_fields = ('user', 'fantasy_points', 'draft_group', 'lineup_players',)
    list_filter = ['created', 'updated']

    @staticmethod
    def lineup_players(obj):
        player_display = mark_safe("<ul>")
        sport = obj.draft_group.salary_pool.site_sport
        site_sport_manager = SiteSportManager()
        player_stats_classes = site_sport_manager.get_player_stats_class(sport)
        print(player_stats_classes)

        if obj.draft_group.start >= timezone.now():
            return "Cannot view the players in a lineup until it's draft group has started."

        for player in obj.players.all():
            player_stats = []

            for stats_class in player_stats_classes:
                game_srid = player.draft_group_player.game_team.game_srid
                player_stats_objects = stats_class.objects.filter(
                    srid_player=player.player.srid,
                    srid_game=game_srid
                )
                for player_stats_object in player_stats_objects:
                    player_stats.append(player_stats_object.to_json())

            player_display += format_html(
                "<li>"
                "<strong>Roster Spot:</strong> {}<br />"
                "<strong>sport.models.player:</strong> {}<br />    "
                "<strong>draftgroup.models.player:</strong> {} <br />"
                "<strong>sport.models.player_stats:</strong> {} <br /><br />"
                "</li>",
                player.roster_spot,
                "%s" % player.player,
                "%s" % player.draft_group_player,
                "%s" % player_stats,
            )

        player_display += mark_safe("</ul>")
        return player_display


admin.site.register(Lineup, LineupAdmin)
