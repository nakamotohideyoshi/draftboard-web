from django.contrib import admin

from .models import SalaryConfig, TrailingGameWeight, Pool, Salary
import sports.classes
from sports.models import Player
import mysite.mixins.generic_search
import django.db.utils
from .tasks import generate_salary
import celery.states
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
    list_display = ['name', 'created']
    inlines = [
        TrailingGameWeightInline,
    ]
    model = SalaryConfig



@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ['site_sport', 'generating_salary', 'active', 'salary_config', 'created']
    model = Pool
    exclude = ('generate_salary_task_id',)
    inlines = [SalaryInline,]

    def generate_salaries(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(request, 'You must select only one pool to generate salaries for at a time.')
        else:
            for pool in queryset:
                task = generate_salary.delay(pool)
                pool.generate_salary_task_id = task.id
                print("task.id "+task.id)
                pool.save()

    def generating_salary(self, obj):
        if obj.generate_salary_task_id is None:
            return ""
        result = generate_salary.AsyncResult(obj.generate_salary_task_id)
        status = result.status
        if status == celery.states.SUCCESS:
            obj.generate_salary_task_id = None
            obj.save()
            return celery.states.SUCCESS
        elif status == celery.states.FAILURE or status == celery.states.STARTED:
            return status
        return ""

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
