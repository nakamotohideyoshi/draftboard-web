from django.contrib import admin

# Register your models here.

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['srid','position','first_name','last_name']
