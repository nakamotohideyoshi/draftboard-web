# cash/admin.py

from django.contrib import admin
from cash.models import CashTransactionDetail, CashBalance, AdminCashDeposit
from cash.forms import AdminCashDepositForm

@admin.register(CashTransactionDetail)
class CashTransactionDetailAdmin(admin.ModelAdmin):

    list_display = ['user','amount','transaction']


@admin.register(CashBalance)
class CashBalanceAdmin(admin.ModelAdmin):

    list_display = ['user','amount']

@admin.register(AdminCashDeposit)
class AdminCashDepositFormAdmin(admin.ModelAdmin):
    """
    this admin model is used for depositing cash
    """
    form = AdminCashDepositForm

    list_display = ['user','amount','reason']

