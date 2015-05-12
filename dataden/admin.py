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

