# cash.tax/admin.py

from django.contrib import admin
from cash.tax.models import (
    Tax,
    TaxForm1099
)

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):

    list_display = ['user','tax_identifier','created']

@admin.register(TaxForm1099)
class TaxAdmin(admin.ModelAdmin):

    list_display = ['created', 'updated', 'user', 'year', 'sent', 'net_profit']
    list_filter = ['user','year','sent']