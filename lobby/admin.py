#
# lobby/admin.py

from django.contrib import admin
import lobby.models

@admin.register(lobby.models.ContestBanner)
class ContestBannerAdmin(admin.ModelAdmin):

    list_display = ['created','modified','internal_description',
                    'start_time','end_time','image_url','links_to']

