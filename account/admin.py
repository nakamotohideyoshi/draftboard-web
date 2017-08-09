from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from account.gidx.models import GidxSession
from account.models import Information, EmailNotification, UserLog, Identity
from cash.admin import CashBalanceAdminInline
from .utils import reset_user_password_email


@admin.register(GidxSession)
class GidxSessionAdmin(admin.ModelAdmin):
    model = GidxSession
    list_display = ['user', 'reason_codes', 'gidx_customer_id', 'service_type', 'device_location',
                    'created']
    search_fields = ['user', 'gidx_customer_id', 'device_location']
    list_filter = ['service_type', 'reason_codes']
    readonly_fields = ['user', 'gidx_customer_id', 'session_id', 'service_type', 'device_location',
                       'request_data', 'created', 'reason_codes', 'response_data']

    # Don't let this be deleted via the admin panel
    def has_delete_permission(self, request, obj=None):
        return False


class InformationAdminInline(admin.TabularInline):
    model = Information
    list_display = ['user', 'inactive', 'exclude_date']

    # Don't let this be deleted via the admin panel
    def has_delete_permission(self, request, obj=None):
        return False


class IdentityAdminInline(admin.TabularInline):
    model = Identity
    readonly_fields = [
        'gidx_customer_id', 'dob', 'country', 'region', 'flagged', 'created', 'status', 'metadata']

    # Don't let this be deleted via the admin panel
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Identity)
class IdentityAdmin(admin.ModelAdmin):
    list_display = ['user', 'dob', 'country', 'region', 'flagged', 'created']
    search_fields = ['user__username', 'country', 'region']
    readonly_fields = ['gidx_customer_id', 'user', 'dob', 'country', 'region', 'status', 'metadata',
                       'created']
    list_filter = ['flagged', 'country', 'region']

    # Don't let this be deleted via the admin panel
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = [
        'category',
        'name',
        'default_value',
        'deprecated'
    ]


def sent_reset_password(modeladmin, request, queryset):
    for user in queryset:
        reset_user_password_email(user, request)


sent_reset_password.short_description = "Sent reset password email"


class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets
    inlines = [
        InformationAdminInline,
        IdentityAdminInline,
        CashBalanceAdminInline,
        # CashTransactionDetailAdminInline,
    ]
    actions = [sent_reset_password]

    # Don't let this be deleted via the admin panel
    # def has_delete_permission(self, request, obj=None):
    #     return False


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)


@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip', 'type', 'action', 'timestamp']
    search_fields = ['ip', 'user__username']
    list_filter = ['timestamp', 'type']
    readonly_fields = ['user', 'ip', 'type', 'action', 'timestamp', 'metadata']

    # Don't let this be deleted via the admin panel
    def has_delete_permission(self, request, obj=None):
        return False
