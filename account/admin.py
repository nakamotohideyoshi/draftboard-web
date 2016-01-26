from django.contrib import admin

from account.models import Information, EmailNotification
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from cash.admin import  CashBalanceAdminInline, CashTransactionDetailAdminInline
class InformationAdminInline(admin.StackedInline):
    model = Information
    list_display = ['user','fullname','address1','address2','city','state','zipcode','dob']

@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = [
        'category',
        'name',
        'default_value',
        'deprecated'
    ]

class MyUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets
    inlines = [
        InformationAdminInline,
        CashBalanceAdminInline,
        CashTransactionDetailAdminInline
    ]
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
