from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from account.models import Information, EmailNotification, UserLog, Identity, Confirmation
from cash.admin import CashBalanceAdminInline, CashTransactionDetailAdminInline
from .utils import reset_user_password_email


class InformationAdminInline(admin.TabularInline):
    model = Information
    list_display = ['user', 'fullname', 'address1', 'address2', 'city', 'state', 'zipcode', 'dob']


class IdentityAdminInline(admin.TabularInline):
    model = Identity
    list_display = ['first_name', 'last_name', 'birth_day', 'birth_month', 'birth_year',
                    'postal_code', 'created']


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
        CashTransactionDetailAdminInline,
    ]
    actions = [sent_reset_password]

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)


@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip', 'type', 'action', 'timestamp']
    search_fields = ['ip', 'user__username']
    list_filter = ['timestamp', 'type']

admin.site.register(Confirmation)