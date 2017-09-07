from django.contrib import admin

from transaction.models import TransactionType, Transaction


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ['category', 'name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'created', 'action_that_created_transaction',
                    'transaction_detail_objects',
                    'category']
    readonly_fields = ['user', 'category', 'created', 'transaction_detail_objects', 'action_that_created_transaction']

    @staticmethod
    def action_that_created_transaction(obj):
        return obj.action

    @staticmethod
    def transaction_detail_objects(obj):
        return obj.to_json()
