#
# prize/admin.py

from django.contrib import admin

import prize.models

@admin.register(prize.models.PrizeStructure)
class PrizeStructureAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('generator', )
        return self.readonly_fields

@admin.register(prize.models.Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ['prize_structure','rank','amount']
    list_filter = ['prize_structure']

@admin.register(prize.models.CreateTicketPrizeStructure)
class CreateTicketPrizeStructureAdmin(admin.ModelAdmin):
    list_display = ['ticket_value','num_prizes']