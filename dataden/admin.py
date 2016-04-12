#
# dataden/admin.py

from django.contrib import admin
import dataden.models

@admin.register(dataden.models.Trigger)
class TriggerAdmin(admin.ModelAdmin):
    list_display = ['enabled', 'ns', 'parent_api']

@admin.register(dataden.models.LiveStatsCacheConfig)
class LiveStatsCacheConfigAdmin(admin.ModelAdmin):
    list_display = ['updated','key_timeout','timeout_mod']

@admin.register(dataden.models.PbpDebug)
class LiveStatsCacheConfigAdmin(admin.ModelAdmin):
    list_display = [
        'created',
        'url',
        'game_srid',
        'srid',
        'description',
        'xml_str',
    ]

    list_filter = [
        'created',
        'url',
        'game_srid',
        'srid',
    ]

    search_fields = [
        'url',
        'game_srid',
        'srid',
        'description',
    ]

