# transaction/admin.py

from django.contrib import admin
from transaction.models import TransactionType, Transaction

@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):

    list_display = ['category','name']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = ['user','category']
