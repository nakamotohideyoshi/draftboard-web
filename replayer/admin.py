#
# replayer/admin.py

from django.contrib import admin
import replayer.models

@admin.register(replayer.models.Replay)
class ReplayAdmin(admin.ModelAdmin):
    list_display = ['name','start','end']

@admin.register(replayer.models.Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ['ts','ns','o']