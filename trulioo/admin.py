#
# admin.py

from django.contrib import admin
import trulioo.models

@admin.register(trulioo.models.Verification)
class VerificationAdmin(admin.ModelAdmin):

    list_display = ['created','user','transaction','transaction_record','record_status']
    list_filter = ['created','user','record_status']