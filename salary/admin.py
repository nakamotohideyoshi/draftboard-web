#
# salary/admin.py

from django.contrib import admin
from django.db.transaction import atomic
from .models import SalaryConfig, TrailingGameWeight, Pool, Salary
import sports.classes
from sports.models import Player
import mysite.mixins.generic_search
import django.db.utils
from .tasks import generate_salaries_for_sport # generate_salary
import celery.states
from django.utils.html import format_html
from salary.classes import (
    OwnershipPercentageAdjuster,
)

class TrailingGameWeightInline(admin.TabularInline):
    model = TrailingGameWeight

class PlayerInline(admin.TabularInline):
    model = Player

class SalaryInline(admin.TabularInline):
    model = Salary
    can_delete = False
    extra = 0
    readonly_fields = ('player', 'primary_roster', 'fppg')
                    # + ('flagged','amount','amount_unadjusted','ownership_percentage')
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
    list_display = ['site_sport', 'generating_salary', 'active', 'salary_config', 'download_csv', 'created']
    model = Pool
    exclude = ('generate_salary_task_id',)
    inlines = [SalaryInline,]

    def download_csv(self, obj):
        return format_html('<a href="{}" class="btn btn-success">{}</a>',
                            "/api/salary/export-pool-csv/%s/" % str(obj.pk), "Download .csv" )

    def generate_salaries(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(request, 'You must select only one pool to generate salaries for at a time.')
        else:
            for pool in queryset:
                #task = generate_salary.delay(pool)
                task = generate_salaries_for_sport.delay(pool.site_sport.name)
                pool.generate_salary_task_id = task.id
                print("task.id "+task.id)
                pool.save()

    @atomic
    def apply_ownership_adjustment(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, 'Select a single pool to apply the ownership adjustment.')
        else:
            for pool in queryset:
                opa = OwnershipPercentageAdjuster(pool)
                opa.update()

    def generating_salary(self, obj):
        if obj.generate_salary_task_id is None:
            return ""
        result = generate_salaries_for_sport.AsyncResult(obj.generate_salary_task_id)
        status = result.status
        if status == celery.states.SUCCESS:
            obj.generate_salary_task_id = None
            obj.save()
            return celery.states.SUCCESS
        elif status == celery.states.FAILURE or status == celery.states.STARTED:
            return status
        return ""

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []
        else:
            return [inline(self.model, self.admin_site) for inline in self.inlines]

    def generate_salaries_and_adjust_for_ownership(self, *args, **kwargs):
        """
        condense the two actions into 1 step for ease.
        """
        self.generate_salaries(*args, **kwargs)
        self.apply_ownership_adjustment(*args, **kwargs)

    def reset_ownership_adjustment(self, request, queryset):
        """
        unapplies all ownership adjustments, setting the salaries
        back to their original values
        """
        if queryset.count() != 1:
            self.message_user(request, 'Select a single pool to apply the ownership adjustment.')
        else:
            for pool in queryset:
                opa = OwnershipPercentageAdjuster(pool)
                opa.reset()

    #
    # admin actions in dropdown
    actions = [
        generate_salaries,
        apply_ownership_adjustment,
        reset_ownership_adjustment,
        generate_salaries_and_adjust_for_ownership,
    ]
    list_filter = ['salary__flagged', 'salary__primary_roster']

@admin.register(Salary)
class SalaryAdmin(mysite.mixins.generic_search.GenericSearchMixin, admin.ModelAdmin):

    list_display    = ['player','amount','flagged','pool', 'primary_roster', 'fppg']
    list_editable   = ['amount', 'flagged']
    model           = Salary
    list_filter     = [ 'primary_roster', 'flagged', 'pool']
    raw_id_admin    = ('pool',)
    search_fields   = ('player__first_name', 'player__last_name')

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
