#
# ticket/admin.py

from django.contrib import admin
import ticket.models

@admin.register(ticket.models.TicketAmount)
class TicketAmountAdmin(admin.ModelAdmin):
    list_display = ['amount']


