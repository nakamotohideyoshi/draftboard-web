#
# sports/mlb/admin.py

from django.contrib import admin
import sports.mlb.models

@admin.register(sports.mlb.models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['srid','market','name']

@admin.register(sports.mlb.models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['srid','start','home','away','day_night','game_number']

@admin.register(sports.mlb.models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['srid','preferred_name','first_name','last_name']

@admin.register(sports.mlb.models.PlayerStatsHitter)
class PlayerStatsHitterAdmin(admin.ModelAdmin):
    list_display = ['game','player','bb','s','d','t','hr','rbi','r','hbp','sb','cs','ktotal','ab','ap','lob','xbh']

@admin.register(sports.mlb.models.PlayerStatsPitcher)
class PlayerStatsPitcherAdmin(admin.ModelAdmin):
    list_display = ['game','player','ip_1','ip_2','win','loss','qstart','ktotal','er','h','bb','hbp','cg','cgso','nono']

