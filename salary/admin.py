from raven.contrib.django.raven_compat.models import client
from django.contrib import (
    admin,
    messages,
)
from django.db.transaction import atomic
from .models import SalaryConfig, TrailingGameWeight, Pool, Salary
import sports.classes
from sports.models import Player
import mysite.mixins.generic_search
import django.db.utils
from .tasks import (
    generate_salaries_for_sport,
    generate_salaries_from_statscom_projections_nfl,
    generate_salaries_from_statscom_projections_nba,
)
import celery.states
from django.utils.html import format_html
from salary.classes import (
    OwnershipPercentageAdjuster,
)
from logging import getLogger

logger = getLogger('salary.admin')


# @admin.register(TrailingGameWeight)
# class TrailingGameWeightAdmin(admin.ModelAdmin):
#     list_display = ['salary', 'through', 'weight']


# class TrailingGameWeightInline(admin.TabularInline):
#     model = TrailingGameWeight

class TrailingGameWeightInline(admin.TabularInline):
    model = TrailingGameWeight
    extra = 1
    list_display = ['through', 'weight']
    # readonly_fields = ['through','weight']


class PlayerInline(admin.TabularInline):
    model = Player


class SalaryInline(admin.TabularInline):
    model = Salary
    can_delete = False
    extra = 0
    readonly_fields = (
        'updated_at',
        'sal_dk',
        'sal_fd',
        'player',
        'primary_roster',
        # 'fppg_pos_weighted',      # deprecated, doesnt apply to stats.com projections
        'fppg',
        'avg_fppg_for_position',
        # 'num_games_included',     # deprecated, doesnt apply to stats.com projections
        'amount_unadjusted',
        'ownership_percentage',

        'random_adjust_amount',

    )
    # + ('flagged','amount','amount_unadjusted','ownership_percentage')

    exclude = ('player_id', 'player_type', 'player', 'fppg_pos_weighted', 'num_games_included')

    def get_queryset(self, request):
        # select_related('priced_product__product')
        return super().get_queryset(request).prefetch_related('player', 'pool', 'primary_roster').order_by('-amount')

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
    list_display = ['site_sport', 'generating_salary', 'active', 'salary_config', 'download_csv']
    model = Pool
    exclude = ('generate_salary_task_id',)
    inlines = [SalaryInline, ]

    def download_csv(self, obj):
        return format_html('<a href="{}" class="btn btn-success">{}</a>',
                           "/api/salary/export-pool-csv/%s/" % str(obj.pk), "Download .csv")

    def OLD_generate_salaries(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(
                request, 'You must select only one pool to generate salaries for at a time.')
        else:
            for pool in queryset:
                # task = generate_salary.delay(pool)
                task = generate_salaries_for_sport.delay(pool.site_sport.name)
                pool.generate_salary_task_id = task.id
                print("task.id " + task.id)
                pool.save()

    @atomic
    def apply_ownership_adjustment(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, 'Select a single pool to apply the ownership adjustment.')
        else:
            for pool in queryset:
                opa = OwnershipPercentageAdjuster(pool)
                updated_count = opa.update()
                # msg the admin with a note about how many were updated
                msg = '%s players updated.' % str(updated_count)
                messages.success(request, msg)

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

    # def generate_salaries_and_adjust_for_ownership(self, *args, **kwargs):
    #     """
    #     condense the two actions into 1 step for ease.
    #     """
    #     self.generate_salaries(*args, **kwargs)
    #     self.apply_ownership_adjustment(*args, **kwargs)

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

    def generate_salaries_using_STATScom_Projections(self, request, queryset):
        """
        admin action to generate salaries for the selected pool based on stats.com fantasy
        projections

        :param request:
        :param queryset:
        :return:
        """
        logger.info('action: salary.admin.generate_salaries_using_STATScom_Projections')

        if len(queryset) > 1:
            logger.warn('You must select only one pool to generate salaries for at a time.')
            self.message_user(
                request, 'You must select only one pool to generate salaries for at a time.')
        else:
            # should be a list of 1 item.
            for pool in queryset:

                sport = pool.site_sport.name
                if sport == 'nfl':
                    logger.info('Queing NFL stats projection task.')
                    # use STATS.com fantasy projections api as the basis for draftboard player
                    # salaries
                    task_result = generate_salaries_from_statscom_projections_nfl.delay()

                elif sport == 'nba':
                    logger.info('Queing NBA stats projection task.')
                    task_result = generate_salaries_from_statscom_projections_nba.delay()

                else:
                    msg = '[%s] is unimplemented server-side. DID NOT GENERATE SALARIES for %s!' % (
                        sport, sport)
                    logger.error(msg)
                    client.captureMessage(msg)
                    self.message_user(request, msg)
                    return

                # get() is blocking and waits for task to finish
                task_result.get()
                logger.info('stats projection task has finished, returning to client.')
                # task finished. presumably salaries have been updated based on latest projections
                messages.success(request, 'updated salaries')

    #
    # admin actions in dropdown
    actions = [
        generate_salaries_using_STATScom_Projections,

        apply_ownership_adjustment,
        reset_ownership_adjustment,

        OLD_generate_salaries,
        # generate_salaries_and_adjust_for_ownership,
    ]
    list_filter = ['salary__flagged', 'salary__primary_roster']


@admin.register(Salary)
class SalaryAdmin(mysite.mixins.generic_search.GenericSearchMixin, admin.ModelAdmin):
    list_display = ['player', 'amount', 'flagged', 'pool',
                    'primary_roster', 'random_adjust_amount', 'fppg_pos_weighted', 'fppg', 'avg_fppg_for_position',
                    'num_games_included', 'updated_at']
    list_editable = ['amount', 'flagged']
    model = Salary
    list_filter = ['primary_roster', 'flagged', 'pool']
    raw_id_admin = ('pool',)
    search_fields = ('player__first_name', 'player__last_name')

    def has_add_permission(self, request):
        return False

    try:
        related_search_mapping = {
            'player': {
                'content_type': 'player_type',
                'object_id': 'player_id',
                'ctypes': sports.classes.SiteSportManager().get_player_classes()
            }
        }
    except (django.db.utils.OperationalError, django.db.utils.ProgrammingError):
        # relation "django_content_type" does not exist
        print('relation "django_content_type" does not exist - this should only happen on the first migrate!')
