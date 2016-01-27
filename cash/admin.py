# cash/admin.py

from django.contrib import admin
from cash.models import CashTransactionDetail, CashBalance, AdminCashDeposit, \
                         BraintreeTransaction, AdminCashWithdrawal
from cash.forms import AdminCashDepositForm, AdminCashWithdrawalForm
from contest.payout.models import Payout,FPP,Rake
from contest.buyin.models import Buyin
@admin.register(CashTransactionDetail)
class CashTransactionDetailAdmin(admin.ModelAdmin):

    list_display = ['user','amount','transaction_identifier','transaction_info', 'created']
    search_fields = ('user__username',)
    readonly_fields = ['user', 'amount', 'transaction','created']

    def transaction_info(self, obj):
        arr_classes = [Buyin, Payout, Rake, FPP]

        for class_action in arr_classes:
            try:
                val = class_action.objects.get(transaction=obj.transaction)
                return type(val).__name__ + ": "+val.contest.name
            except class_action.DoesNotExist:
                pass
        if obj.amount > 0:
            return "Deposit"
        else:
            return "Withdrawal"

    def transaction_identifier(self, obj):
        return obj.transaction.pk

    def has_delete_permission(self, request, obj=None):
       return False

    def has_add_permission(self, request):
        return False



    transaction_info.short_description = "Transaction Info"
    transaction_identifier.short_description = "Transaction Id"


class CashTransactionDetailAdminInline(admin.TabularInline):
    model = CashTransactionDetail
    list_display = [ 'amount','transaction_info', 'created']
    readonly_fields = [ 'amount','transaction_info', 'created']
    exclude = ('transaction',)


    def has_delete_permission(self, request, obj=None):
       return False

    def has_add_permission(self, request):
        return False

    def transaction_info(self, obj):
        arr_classes = [Buyin, Payout, Rake, FPP]

        for class_action in arr_classes:
            try:
                val = class_action.objects.get(transaction=obj.transaction)
                return type(val).__name__ + ": "+val.contest.name
            except class_action.DoesNotExist:
                pass
        if obj.amount > 0:
            return "Deposit"
        else:
            return "Withdrawal"




class CashBalanceAdminInline(admin.StackedInline):
    verbose_name = "Cash Balance"
    model = CashBalance
    readonly_fields = ['user','amount']
    list_display = ['user','amount']

    def has_delete_permission(self, request, obj=None):
       return False


@admin.register(AdminCashDeposit)
class AdminCashDepositFormAdmin(admin.ModelAdmin):
    """
    this admin model is used for depositing cash
    """
    form = AdminCashDepositForm

    #list_display = ['created','user','amount','reason']
    list_display = ['user','amount','reason']

    raw_id_fields = ('user',)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AdminCashWithdrawal)
class AdminCashWithdrawalFormAdmin(admin.ModelAdmin):
    """
    this admin model is used for withdrawing cash
    """
    form = AdminCashWithdrawalForm

    #list_display = ['created','user','amount','reason']
    list_display = ['user','amount','reason']

    def has_delete_permission(self, request, obj=None):
        return False


# @admin.register(BraintreeTransaction)
# class BraintreeTransactionAdmin(admin.ModelAdmin):
#
#     list_display = ['created','transaction','braintree_transaction']