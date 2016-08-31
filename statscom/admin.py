#
# admin.py

from django.contrib import admin
import statscom.models

@admin.register(statscom.models.PlayerLookup)
class PlayerLookupAdmin(admin.ModelAdmin):
    list_display = ['created','updated','player','pid']
    list_filter = ['created','updated','pid']
