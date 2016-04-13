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

    show_full_result_count = True

    list_display = [
        'created',
        'game_srid',
        'srid',
        'description',
        'xml_str',
        'timestamp_pushered',
        'delta_seconds',
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

    def delta_seconds(self, pbpdebug):
        return pbpdebug.get_delta_seconds()