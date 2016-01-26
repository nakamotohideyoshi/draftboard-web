from django.contrib import admin
import sports.models

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