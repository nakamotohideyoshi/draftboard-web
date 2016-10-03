from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from account.models import Information, EmailNotification, UserLog
from cash.admin import CashBalanceAdminInline, CashTransactionDetailAdminInline


class InformationAdminInline(admin.TabularInline):
    model = Information
    list_display = ['user','fullname','address1','address2','city','state','zipcode','dob']


class UserLogAdminInline(admin.TabularInline):
    model = UserLog
    list_display = ['ip', 'action', 'type', 'timestamp', 'metadata']
    readonly_fields = ('ip', 'action', 'type', 'timestamp', 'metadata')
    can_delete = False
    extra = 0
    max_num = 10

    def has_add_permission(self, request):
        return False


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
        CashTransactionDetailAdminInline,
        UserLogAdminInline,
    ]
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)


@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip', 'action', 'type', 'timestamp']
    search_fields = ['ip', 'user__email', 'user__first_name', 'user__last_name',
                     'metadata']
    list_filter = ['action', 'type', 'timestamp']

