#
# keyprefix/admin.py

from django.contrib import admin
from keyprefix.models import KeyPrefix

@admin.register(KeyPrefix)
class KeyPrefixAdmin(admin.ModelAdmin):
    list_display = ['created','prefix']
