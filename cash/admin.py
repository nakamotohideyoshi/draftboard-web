# cash/admin.py

from django.contrib import admin
from cash.models import CashTransactionDetail, CashBalance

# def create_transaction(modeladmin, request, queryset):
#     pass
# create_transaction.short_description = "cash transaction created"

@admin.register(CashTransactionDetail)
class CashTransactionDetailAdmin(admin.ModelAdmin):

    list_display = ['user','amount','transaction']
    #actions = [create_transaction]


@admin.register(CashBalance)
class CashBalanceAdmin(admin.ModelAdmin):

    list_display = ['user','amount']

