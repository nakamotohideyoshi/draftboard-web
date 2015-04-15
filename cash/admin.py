# cash/admin.py

from django.contrib import admin
from cash.models import CashTransactionDetail, CashBalance, AdminCashDeposit, \
                         BraintreeTransaction
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

    #list_display = ['created','user','amount','reason']
    list_display = ['user','amount','reason']

@admin.register(BraintreeTransaction)
class BraintreeTransactionAdmin(admin.ModelAdmin):

    list_display = ['created','transaction','braintree_transaction']