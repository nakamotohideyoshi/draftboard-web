from django.contrib import admin

from account.models import Information, EmailNotification

@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    list_display = ['user','fullname','address1','address2','city','state','zipcode','dob']

@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = [
        'category',
        'name',
        'default_value',
        'deprecated'
    ]