from django.contrib import admin

# Register your models here.
from .models import SalaryConfig, TrailingGameWeight, Pool, Salary

@admin.register(SalaryConfig)
class SalaryConfigAdmin(admin.ModelAdmin):
    list_display    = ['id','trailing_games', 'days_since_last_game_flag',
                       'min_games_flag', 'min_player_salary',
                       'max_team_salary','min_avg_fppg_allowed_for_avg_calc']

    model           = SalaryConfig

@admin.register(TrailingGameWeight)
class TrailingGameWeightAdmin(admin.ModelAdmin):
    list_display    = ['id','salary', 'through', 'weight']
    model           = TrailingGameWeight

@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display    = ['id','created', 'site_sport', 'active', 'salary_config' ]
    model = Pool

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display    = ['id','created', 'pool', 'amount', 'flagged', 'player' ]
    model = Salary

