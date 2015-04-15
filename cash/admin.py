# cash/admin.py

from django.contrib import admin
from cash.models import CashTransactionDetail, CashBalance, AdminCashDeposit, AdminCashWithdrawal
from cash.forms import AdminCashDepositForm, AdminCashWithdrawalForm

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

    #list_display = ['created','user','amount','reason']
    list_display = ['user','amount','reason']

@admin.register(AdminCashWithdrawal)
class AdminCashWithdrawalFormAdmin(admin.ModelAdmin):
    """
    this admin model is used for withdrawing cash
    """
    form = AdminCashWithdrawalForm

    #list_display = ['created','user','amount','reason']
    list_display = ['user','amount','reason']

