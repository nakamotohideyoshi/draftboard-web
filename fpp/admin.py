# fpp/admin.py

from django.contrib import admin
from fpp.models import FppTransactionDetail, FppBalance, \
                        AdminFppDeposit, AdminFppWithdraw
from fpp.forms import AdminFppDepositForm, AdminFppWithdrawForm


@admin.register(FppTransactionDetail)
class FppTransactionDetailAdmin(admin.ModelAdmin):

    list_display = ['user', 'amount', 'transaction']
    search_fields = ['user__username']
    readonly_fields = ['user', 'amount', 'transaction']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(FppBalance)
class FppBalanceAdmin(admin.ModelAdmin):
    list_display = ['user','amount']
    search_fields = ['user__username']
    readonly_fields = ['user','amount']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(AdminFppDeposit)
class AdminFppDepositFormAdmin(admin.ModelAdmin):
    """
    this admin model is used for depositing Fpp
    """
    form = AdminFppDepositForm

    list_display = ['user','amount','reason']
    search_fields = ['user__username']

    def has_delete_permission(self, request, obj=None):
        return False



@admin.register(AdminFppWithdraw)
class AdminFppWithdrawFormAdmin(admin.ModelAdmin):
    """
    this admin model is used for withdrawing Fpp
    """
    form = AdminFppWithdrawForm

    list_display = ['user','amount','reason']
    search_fields = ['user__username']

    def has_delete_permission(self, request, obj=None):
        return False