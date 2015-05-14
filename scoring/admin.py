#
# scoring/admin.py

from django.contrib import admin
import scoring.models

@admin.register(scoring.models.ScoreSystem)
class ScoreSystemAdmin(admin.ModelAdmin):
    list_display = ['sport','name','description']

@admin.register(scoring.models.StatPoint)
class StatPointAdmin(admin.ModelAdmin):
    list_display = ['score_system','stat','value']