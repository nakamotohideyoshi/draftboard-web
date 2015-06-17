#
# prize/admin.py

from django.contrib import admin

import prize.models

@admin.register(prize.models.PrizeStructure)
class PrizeStructureAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(prize.models.Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ['rank','amount']
