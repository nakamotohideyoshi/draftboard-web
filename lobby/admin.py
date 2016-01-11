#
# lobby/admin.py

from django.contrib import admin
import lobby.models

#
# all banners should have these common fields
COMMON_BANNER_FIELDS = [
    'created',
    'modified',
    'internal_description',
    'start_time',
    'end_time',
    'image_url'
]

@admin.register(lobby.models.ContestBanner)
class ContestBannerAdmin(admin.ModelAdmin):

    list_display = COMMON_BANNER_FIELDS + ['links_to']

