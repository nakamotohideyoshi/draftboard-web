#
# draftgroup/admin.py

from django.contrib import admin
import draftgroup.models

@admin.register(draftgroup.models.DraftGroup)
class DraftGroupAdmin(admin.ModelAdmin):
    list_display = ['created','salary_pool','start','end']

@admin.register(draftgroup.models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['created','draft_group','player','salary']

@admin.register(draftgroup.models.GameTeam)
class GameTeamAdmin(admin.ModelAdmin):
    list_display = ['created','draft_group','game_srid','start','alias','team_srid']

@admin.register(draftgroup.models.PlayerUpdate)
class PlayerUpdateAdmin(admin.ModelAdmin):
    list_display = ['created','update_id','player_srid','category','type','value']
    list_filter = ['created','category','type','player_srid']
    search_fields = ['update_id','player_srid','category','type','value']

@admin.register(draftgroup.models.GameUpdate)
class GameUpdateAdmin(admin.ModelAdmin):
    list_display = ['created','update_id','game_srid','category','type','value']
    list_filter = ['created','category','type','game_srid']
    search_fields = ['update_id','game_srid','category','type','value']