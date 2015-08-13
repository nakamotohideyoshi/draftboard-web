from django.contrib import admin
from .models import RosterSpotPosition, RosterSpot

class RosterSpotPositionInline(admin.TabularInline):
    model = RosterSpotPosition

@admin.register(RosterSpot)
class RosterSportAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'site_sport', 'amount', 'idx']
    inlines = [
        RosterSpotPositionInline,
    ]
    model = RosterSpot

@admin.register(RosterSpotPosition)
class RosterSpotPositionAdmin(admin.ModelAdmin):
    list_display = [ 'roster_spot', 'position', 'is_primary' ]

