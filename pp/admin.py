#
# admin.py

from django.contrib import admin
from pp.models import (
    SavedCardPaymentData,
    CreditCardPaymentData,
    PayPalAccountPaymentData,
)

PAYMENT_DATA_LIST_DISPLAY = ['created','payment_data']

@admin.register(SavedCardPaymentData)
class SavedCardPaymentDataAdmin(admin.ModelAdmin):
    list_display = PAYMENT_DATA_LIST_DISPLAY

@admin.register(CreditCardPaymentData)
class CreditCardPaymentDataAdmin(admin.ModelAdmin):
    list_display = PAYMENT_DATA_LIST_DISPLAY

@admin.register(PayPalAccountPaymentData)
class PayPalAccountPaymentDataAdmin(admin.ModelAdmin):
    list_display = PAYMENT_DATA_LIST_DISPLAY