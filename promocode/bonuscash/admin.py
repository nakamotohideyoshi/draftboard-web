# promocode/bonuscash/admin.py

from django.contrib import admin
from promocode.bonuscash.models import BonusCashTransactionDetail, BonusCashBalance, \
    AdminBonusCashDeposit, AdminBonusCashWithdraw
from promocode.bonuscash.forms import AdminBonusCashDepositForm, AdminBonusCashWithdrawForm


@admin.register(BonusCashTransactionDetail)
class BonusCashTransactionDetailAdmin(admin.ModelAdmin):

    list_display = ['user', 'amount', 'transaction']


@admin.register(BonusCashBalance)
class BonusCashBalanceAdmin(admin.ModelAdmin):

    list_display = ['user', 'amount']


@admin.register(AdminBonusCashDeposit)
class AdminBonusCashDepositFormAdmin(admin.ModelAdmin):
    """
    this admin model is used for depositing bonuscash
    """
    form = AdminBonusCashDepositForm

    list_display = ['user', 'amount', 'reason']


@admin.register(AdminBonusCashWithdraw)
class AdminBonusCashWithdrawFormAdmin(admin.ModelAdmin):
    """
    this admin model is used for withdrawing bonuscash
    """
    form = AdminBonusCashWithdrawForm
    search_fields = ['user__username']
    list_display = ['user', 'amount', 'reason', 'created']
    raw_id_fields = ("user",)
