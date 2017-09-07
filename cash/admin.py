from django.contrib import admin

from cash.forms import AdminCashDepositForm, AdminCashWithdrawalForm
from cash.models import (
    CashTransactionDetail,
    CashBalance,
    AdminCashDeposit,
    AdminCashWithdrawal,
    GidxTransaction,
)
from contest.buyin.models import Buyin
from contest.payout.models import Payout, FPP, Rake
from contest.refund.models import Refund


@admin.register(CashTransactionDetail)
class CashTransactionDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'transaction_pk', 'user', 'amount', 'get_action',  'created',
                    'transaction_category']
    search_fields = ('user__username',)
    readonly_fields = ['user', 'amount', 'transaction', 'created']
    ordering = ('-transaction',)

    @staticmethod
    def transaction_pk(obj):
        return obj.transaction.id

    @staticmethod
    def transaction_category(obj):
        return obj.transaction.category

    def get_action(self, obj):
        return obj.transaction.action

    get_action.short_description = "Action that caused this Transaction"

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class CashTransactionDetailAdminInline(admin.TabularInline):
    model = CashTransactionDetail
    list_display = ['amount', 'transaction', 'transaction_info', 'created']
    readonly_fields = ['amount', 'transaction', 'transaction_info', 'created']

    # exclude = ('transaction',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    @staticmethod
    def transaction_info(obj):
        arr_classes = [Buyin, Payout, Rake, FPP, Refund, GidxTransaction]

        for class_action in arr_classes:
            try:
                val = class_action.objects.get(transaction=obj.transaction)
                return type(val).__name__ + ": " + val.contest.name
            except class_action.DoesNotExist:
                pass
        if obj.amount > 0:
            return "Deposit"
        else:
            return "Withdrawal"


class CashBalanceAdminInline(admin.StackedInline):
    verbose_name = "Cash Balance"
    model = CashBalance
    readonly_fields = ['user', 'amount']
    list_display = ['user', 'amount']

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CashBalance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'updated']


@admin.register(AdminCashDeposit)
class AdminCashDepositFormAdmin(admin.ModelAdmin):
    """
    this admin model is used for depositing cash
    """
    form = AdminCashDepositForm

    # list_display = ['created','user','amount','reason']
    list_display = ['user', 'amount', 'reason']

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AdminCashWithdrawal)
class AdminCashWithdrawalFormAdmin(admin.ModelAdmin):
    """
    this admin model is used for withdrawing cash
    """
    form = AdminCashWithdrawalForm

    # list_display = ['created','user','amount','reason']
    list_display = ['user', 'amount', 'reason']

    def has_delete_permission(self, request, obj=None):
        return False


# @admin.register(BraintreeTransaction)
# class BraintreeTransactionAdmin(admin.ModelAdmin):
#
#     list_display = ['created','transaction','braintree_transaction']

@admin.register(GidxTransaction)
class GidxTransaction(admin.ModelAdmin):
    readonly_fields = ['created', 'transaction', 'merchant_transaction_id']
    list_display = ['created', 'transaction', 'merchant_transaction_id']
    # inlines = [CashTransactionDetailAdminInline]
