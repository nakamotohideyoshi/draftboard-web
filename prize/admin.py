from django.contrib import admin
import prize.models


class RankAdminInline(admin.TabularInline):
    model = prize.models.Rank
    list_display = ['prize_structure', 'rank', 'amount']
    list_filter = ['prize_structure']
    exclude = ['amount_id']
    readonly_fields = ['prize_structure', 'rank', 'amount', 'amount_type']

    def has_add_permission(self, request): # removes Add button
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(prize.models.PrizeStructure)
class PrizeStructureAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    inlines = [RankAdminInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('generator',)
        return self.readonly_fields

    def has_add_permission(self, request): # removes Add button
        return False


@admin.register(prize.models.CreateTicketPrizeStructure)
class CreateTicketPrizeStructureAdmin(admin.ModelAdmin):
    list_display = ['ticket_value', 'num_prizes']
