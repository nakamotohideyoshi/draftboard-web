from django.contrib import admin

from .models import SalaryConfig, TrailingGameWeight, Pool, Salary
from .classes import  SalaryGenerator
import sports.classes
from sports.models import Player
import mysite.mixins.generic_search
import django.db.utils

class TrailingGameWeightInline(admin.TabularInline):
    model = TrailingGameWeight

class PlayerInline(admin.TabularInline):
    model = Player

class SalaryInline(admin.TabularInline):
    model = Salary
    extra = 0
    readonly_fields = ('player', 'primary_roster', 'fppg')
    exclude = ('player_id', 'player_type')
    def player(self, obj):
        return obj.player


    def has_add_permission(self, request):
        return False



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
            self.message_user(request, 'You must select only one pool to generate salaries for at a time.')
        else:
            for pool in queryset:
                ssm = sports.classes.SiteSportManager()
                player_stats_class = ssm.get_player_stats_class(pool.site_sport)
                sg = SalaryGenerator(player_stats_class, pool)
                sg.generate_salaries()

    actions = [generate_salaries, ]
    list_filter = ['salary__flagged', 'salary__primary_roster']

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []
        else:
            return  [inline(self.model, self.admin_site) for inline in self.inlines]



@admin.register(Salary)
class SalaryAdmin(mysite.mixins.generic_search.GenericSearchMixin, admin.ModelAdmin):
    list_display = ['player','amount','flagged','pool', 'primary_roster', 'fppg']
    list_editable = ['amount', 'flagged']
    model = Salary
    list_filter = [ 'primary_roster', 'flagged', 'pool']
    raw_id_admin = ('pool', )
    search_fields = ('player__first_name', 'player__last_name')
    def has_add_permission(self, request):
        return False


    try:
        related_search_mapping = {
            'player': {
                'content_type':'player_type',
                'object_id': 'player_id',
                'ctypes': sports.classes.SiteSportManager().get_player_classes()
            }
        }
    except django.db.utils.ProgrammingError:
        # relation "django_content_type" does not exist
        print('relation "django_content_type" does not exist - this should only happen on the first migrate!')
