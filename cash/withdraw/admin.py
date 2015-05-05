# cash.withdraw/admin.py

from django.contrib import admin
from django.contrib.auth.models import User
from cash.withdraw.models import WithdrawStatus, AutomaticWithdraw, PendingWithdrawMax, \
                                                        PayPalWithdraw, CheckWithdraw


import cash.withdraw.classes
# from cash.withdraw.classes import PayPalWithdraw as PpWithdraw
# from cash.withdraw.classes import CheckWithdraw as CkWithdraw

from mysite.exceptions import AdminDoNotDeleteException

from django.contrib.contenttypes.models import ContentType

# special inline kinds for GenericForeignKey fields
from django.contrib.admin import TabularInline, StackedInline
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline

from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.core import urlresolvers

#
# this is actually global for the whole project - dont remove this,
# you can still add the delete_selected to specific models if you want to
admin.site.disable_action('delete_selected')

@admin.register(WithdrawStatus)
class WithdrawStatusAdmin(admin.ModelAdmin):

    list_display    = ['category','name','description']


class CheckWithdrawTabularInline(admin.TabularInline):
    model = CheckWithdraw

class PayPalWithdrawStackedInline(admin.StackedInline):
    model = PayPalWithdraw

@admin.register(CheckWithdraw)
class CheckWithdrawAdmin(admin.ModelAdmin):

    list_display    = ['created','status','amount','user','check_number',
                       'fullname','address1','address2','city','state','zipcode']
    list_editable   = ['check_number'] # to be editable, it must also be in list_display !

    #
    def check_number_entered_and_check_mailed(self, request, queryset):
        processed = 0
        for obj in queryset:
            if obj.check_number:
                ppw = cash.withdraw.classes.CheckWithdraw( pk=obj.pk )
                ppw.payout()
                processed += 1
            else:
                pass
        total = len(queryset)
        self.message_user( request, '%s / %s selected withdraws processed. %s did not have a check_number.' % (
                                        str(processed), str(total), str(total - processed)))
    check_number_entered_and_check_mailed.short_description = 'I mailed the check for the selected withdraw(s).'

    #
    def decline_withdraw_request(self, request, queryset):
        for obj in queryset:
            print( obj.pk, obj.content_type, 'withdraw:', obj.withdraw )

            ppw = cash.withdraw.classes.CheckWithdraw( pk=obj.pk )
            ppw.cancel()

        total = len(queryset)
        self.message_user( request, '%s Check withdraw(s) cancelled and refunded.')
    decline_withdraw_request.short_description = 'Decline & refund the selected check withdraw(s)'

    #
    # add these actions this modeladmin's view
    actions = [ check_number_entered_and_check_mailed, decline_withdraw_request ]

@admin.register(PayPalWithdraw)
class PayPalWithdrawAdmin(admin.ModelAdmin):

    list_display    = ['created','status','amount','user','email','paypal_transaction','get_status','paypal_errors']

    # non PayPalWithdraw models should throw an exception if this is called on them.
    def paypal_confirm_and_send_payout(self, request, queryset):
        processing = 0
        for obj in queryset:
            print( obj.pk, obj.content_type, 'withdraw:', obj.withdraw )

            ppw = cash.withdraw.classes.PayPalWithdraw( pk=obj.pk )
            try:
                ppw.payout()
                processing += 1
            except:
                pass

        total = len(queryset)
        self.message_user( request, '%s / %s selected withdraws are processing. %s could not be processed.' % (
                                        str(processing), str(total), str(total - processing)))
    paypal_confirm_and_send_payout.short_description = 'Confirm and process selected PayPal cashout(s)'

    #
    def decline_withdraw_request(self, request, queryset):
        for obj in queryset:
            print( obj.pk, obj.content_type, 'withdraw:', obj.withdraw )

            ppw = cash.withdraw.classes.PayPalWithdraw( pk=obj.pk )
            ppw.cancel()
        total = len(queryset)
        self.message_user( request, '%s PayPal withdraw(s) cancelled and refunded.' )
    decline_withdraw_request.short_description = 'Decline & refund the selected PayPal withdraw(s)'

    #
    # the 'action' list is where we can specify
    # functions wed like to show in the admin dropdown menu
    actions = [ paypal_confirm_and_send_payout, decline_withdraw_request ]

@admin.register(AutomaticWithdraw)
class AutomaticWithdrawAdmin(admin.ModelAdmin):
    list_display = ['updated','auto_payout_below']
    list_editable = ['auto_payout_below']

@admin.register(PendingWithdrawMax)
class PendingWithdrawMaxAdmin(admin.ModelAdmin):
    list_display = ['updated','max_pending']
    list_editable = ['max_pending']