# fpp/admin.py

from django.contrib import admin
from fpp.models import FppTransactionDetail, FppBalance, \
                        AdminFppDeposit, AdminFppWithdraw

from fpp.forms import AdminFppDepositForm, AdminFppWithdrawForm



@admin.register(FppTransactionDetail)
class FppTransactionDetailAdmin(admin.ModelAdmin):

    list_display = ['user','amount','transaction']


@admin.register(FppBalance)
class FppBalanceAdmin(admin.ModelAdmin):

    list_display = ['user','amount']

@admin.register(AdminFppDeposit)
class AdminFppDepositFormAdmin(admin.ModelAdmin):
    """
    this admin model is used for depositing Fpp
    """
    form = AdminFppDepositForm

    list_display = ['user','amount','reason']

@admin.register(AdminFppWithdraw)
class AdminFppWithdrawFormAdmin(admin.ModelAdmin):
    """
    this admin model is used for withdrawing Fpp
    """
    form = AdminFppWithdrawForm

    list_display = ['user','amount','reason']

