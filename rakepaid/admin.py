#
# rakepaid/admin.py

from django.contrib import admin
import rakepaid.models

@admin.register(rakepaid.models.LoyaltyStatus)
class LoyaltyStatusAdmin(admin.ModelAdmin):
    list_display = ['rank','name','thirty_day_avg','multiplier']

