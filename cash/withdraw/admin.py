# cash.withdraw/admin.py

from django.contrib import admin
from cash.withdraw.models import WithdrawStatus, PayPalWithdraw, CheckWithdraw, ReviewWithdraw
from cash.withdraw.classes import PayPalWithdraw as PpWithdraw


@admin.register(WithdrawStatus)
class WithdrawStatusAdmin(admin.ModelAdmin):

    list_display = ['category', 'name', 'description']

@admin.register(PayPalWithdraw)
class PayPalWithdrawAdmin(admin.ModelAdmin):

    def process_paypal_withdraw(self, request, queryset):
        # admin = request.user
        print('STEVE')
        for obj in queryset:
            ppw = PpWithdraw()

            # validate_withdraw should be called by update_status()
            #ppw.validate_withdraw( obj.cash_transaction_detail.amount )
            ppw.update_status( obj )


        # queryset.update( status=VALUE )

    list_display = ['email', 'paypal_transaction']
    actions = [process_paypal_withdraw]

@admin.register(CheckWithdraw)
class CheckWithdrawAdmin(admin.ModelAdmin):

    list_display = ['check_number', 'fullname', 'address1', 'address2', 'city', 'state', 'zipcode']

@admin.register(ReviewWithdraw)
class ReviewWithdrawAdmin(admin.ModelAdmin):

    list_display = ['email', 'paypal_transaction', 'check_number', 'fullname', 'address1', 'address2',
                    'city', 'state', 'zipcode']
