from django.contrib import admin

# Register your models here.
from .models import SalaryConfig, TrailingGameWeight, Pool, Salary
from .classes import  SalaryGenerator
from sports.classes import SiteSportManager
from django.contrib.contenttypes.admin import GenericTabularInline
from sports.models import Player

class TrailingGameWeightInline(admin.TabularInline):
    model = TrailingGameWeight

class PlayerInline(admin.TabularInline):
    model = Player

class SalaryInline(admin.TabularInline):
    model = Salary
    extra = 0

    def player(self, obj):
        return obj.player

    # TODO add this here if it will let me so it can properly filter player type
    # def get_inline_instances(self, request, obj=None):
    #     if obj is None:
    #         return None
    #     else:
    #         ssm = SiteSportManager()
    #         player_stats_class = ssm.get_player_class(obj.site_sport)
    #         PlayerInline.model = player_stats_class
    #         return [PlayerInline]


@admin.register(SalaryConfig)
class SalaryConfigAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created']
    inlines = [
        TrailingGameWeightInline,
    ]
    model = SalaryConfig



@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ['site_sport', 'active', 'salary_config', 'created']
    model = Pool
    inlines = [SalaryInline,]
    def generate_salaries(self, request, queryset):
        if len(queryset) > 1:
            self.message_user( request, 'You must select only one pool to generate salaries for at a time.')
        else:
            for pool in queryset:
                ssm = SiteSportManager()
                player_stats_class = ssm.get_player_stats_class(pool.site_sport)
                sg = SalaryGenerator(player_stats_class, pool)
                sg.generate_salaries()

    actions = [generate_salaries, ]

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []
        else:
            return  [inline(self.model, self.admin_site) for inline in self.inlines]



@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    # TODO going to need to disable editing of SalaryAdmins if any games point to the Pool that the Salary points to.
    list_display = ['id', 'created', 'pool', 'amount', 'flagged', 'player']
    search_fields = ['pool', 'player']
    model = Salary

    def has_add_permission(self, request):
        return False




