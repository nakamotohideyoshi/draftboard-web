# cash.withdraw/admin.py

from django.contrib import admin
from django.contrib.auth.models import User
from cash.withdraw.models import WithdrawStatus, PayPalWithdraw, CheckWithdraw, \
                                    ReviewPendingWithdraw

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

# @admin.register(WithdrawStatus)
# class WithdrawStatusAdmin(admin.ModelAdmin):
#
#    list_display = ['category', 'name', 'description']

@admin.register(PayPalWithdraw)
class PayPalWithdrawAdmin(admin.ModelAdmin):

    list_display = ['email', 'paypal_transaction']

    # non PayPalWithdraw models should throw an exception if this is called on them.
    def paypal_confirm_and_send_payout(self, request, queryset):
        for obj in queryset:
            print( obj.pk, obj.content_type, 'withdraw:', obj.withdraw )
            ppw = cash.withdraw.classes.PayPalWithdraw( pk=obj.pk )
            ppw.update_status()

    actions = [ paypal_confirm_and_send_payout ]

class PayPalWithdrawInline(GenericStackedInline):
    model = PayPalWithdraw

@admin.register(CheckWithdraw)
class CheckWithdrawAdmin(admin.ModelAdmin):

    list_display    = ['created','cash_transaction_detail','check_number',
                       'fullname','address1','address2','city','state','zipcode']
    list_editable   = ['check_number'] # to be editable, it must also be in list_display !

    #
    def check_number_entered_and_check_mailed(self, request, queryset):
        for obj in queryset:
            print( obj.pk, obj.content_type, 'withdraw:', obj.withdraw )
            ppw = cash.withdraw.classes.CheckWithdraw( pk=obj.pk )
            ppw.update_status()

    actions = [ check_number_entered_and_check_mailed ]

class CheckWithdrawInline(GenericStackedInline):
    model = CheckWithdraw

@admin.register(ReviewPendingWithdraw)
class ReviewPendingWithdrawAdmin(admin.ModelAdmin):
    """
    the base paypal withdraw request record
    """

    list_display    = ['status','review_now','user','withdraw']

    def get_list_display_links(self, request, list_display):
        return None # dont link the first column to the edit page

    def review_now(self, instance):
        ctype = ContentType.objects.get_for_model( instance.content_object ) # get the dynamic withdraw type
        # model_cls = ctype.model_class()
        # example:  ctype.app_label     == 'withdraw'
        # example:  ctype.model         == 'checkwithdraw'
        #
        # if this function call doesnt crash, its a valid url !
        # func, args, kwargs = urlresolvers.resolve( '/admin/withdraw/checkwithdraw/')
        url = '/admin/%s/%s/' % (ctype.app_label, ctype.model)
        a_tag = '<a href="%s">Review %ss</a>' % (url, ctype.model_class().__name__)

        try:
            func, args, kwargs = urlresolvers.resolve( url )
        except:
            a_tag = '<span class="errors">Unkonwn Withdraw Type</span>'

        #print( a_tag )
        return a_tag

    review_now.short_description    = 'Review Link'
    review_now.allow_tags           = True    # True because the output has html tags
