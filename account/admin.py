from django.contrib import admin

from account.models import Information

@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    list_display = ['user','fullname','address1','address2','city','state','zipcode','dob']