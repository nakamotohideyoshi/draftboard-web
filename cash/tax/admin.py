# cash.tax/admin.py

from django.contrib import admin
from cash.tax.models import Tax

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):

    list_display = ['user','tax_identifier','created']