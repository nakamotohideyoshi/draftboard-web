#
# salary/models.py

from django.db import models
import sports.models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from roster.models import RosterSpot


class SalaryConfig(models.Model):
    """
    The class that keeps a Salary algorithm for a specified sport
    """
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField(
        default="",
        null=False,
        help_text="The plain text name of the configuration",
        verbose_name="Name",
        max_length=64
    )

    days_since_last_game_flag = models.PositiveIntegerField(
        null=False,
        help_text="Flag the player if X days since last game played",
        verbose_name="Days Since Last Game Flag"
    )

    min_games_flag = models.PositiveIntegerField(
        null=False,
        help_text="Flag the player if X games have not been played",
        verbose_name="Min Games Flag"
    )

    min_player_salary = models.PositiveIntegerField(
        null=False,
        help_text="The minimum salary a player can be worth.",
        verbose_name="Min Player Salary"
    )

    max_team_salary = models.PositiveIntegerField(
        null=False,
        help_text="The total team salary for drafting",
        verbose_name="Team Salary"
    )

    min_avg_fppg_allowed_for_avg_calc = models.FloatField(
        null=False,
        default=0.0,
        help_text=("The minimum fppg allowed for a players stats to be used to calculate position "
                   "averages."),
        verbose_name="Min FPPG Allowed for Avg Calc"
    )

    trailing_games = models.PositiveIntegerField(
        null=False,
        help_text="The total number of games considered in the trailing weight section.",
        verbose_name="Trailing Games"
    )

    def __str__(self):
        return '<SalaryConfig> id: %s | name: %s' % (self.id, self.name)

    class Meta:
        verbose_name = 'Algorithm'


class TrailingGameWeight(models.Model):
    """
    The weights of the scores for each tier of trailing games
    """
    salary = models.ForeignKey(
        SalaryConfig,
        null=False,
        related_name='trailing_game_weights'
    )

    through = models.PositiveIntegerField(null=False)

    weight = models.FloatField(
        null=False,
        help_text="Multiplier"
    )

    class Meta:
        unique_together = ('salary', 'through')
        ordering = ('through',)


class Pool(models.Model):
    """
    Creating a Pool with active=True will mark the existing active pool False!

    This model keeps track of all the player pools for all the sports and also
    maintains the active player pool status. Only one pool per site_sport can be
    active.
    """
    created = models.DateTimeField(
        auto_now_add=True
    )

    site_sport = models.ForeignKey(
        sports.models.SiteSport,
        null=False
    )

    active = models.BooleanField(
        null=False,
        default=False
    )

    salary_config = models.ForeignKey(
        SalaryConfig,
        null=False
    )

    generate_salary_task_id = models.CharField(
        default=None,
        null=True,
        verbose_name="Generating Salary",
        max_length=255
    )

    #
    # fields for factoring in ownership percentages.
    ownership_threshold_low_cutoff = models.FloatField(
        null=True,
        default=10.0
    )

    low_cutoff_increment = models.FloatField(
        null=True,
        default=1.0
    )

    ownership_threshold_high_cutoff = models.FloatField(
        null=True,
        default=30.0
    )

    high_cutoff_increment = models.FloatField(
        null=True,
        default=1.0
    )

    max_percent_adjust = models.FloatField(
        null=False,
        default=10.0,
        help_text='the maximum percentage shift due to ownership adjustment'
    )

    # randomly add/subtract this much to the final salary (value is % of the salary)
    random_percent_adjust = models.FloatField(
        default=0.0,
        null=False,
        help_text=('if this is non-zero, apply an additional shift to all salaries randomly chosen '
                   'from [-X%, +X% ]. this will happen before the final rounding.')
    )

    # make sure that only one Pool can be active at a time (for the site_sport)
    def save(self, *args, **kwargs):
        if self.active:
            try:
                temp = Pool.objects.get(active=True, site_sport=self.site_sport)
                if self != temp:
                    temp.active = False
                    temp.save()
            except Pool.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return '<Pool id: %s | active: %s | sport: %s | created: %s>' % (
            self.id, self.active, self.site_sport, self.created.strftime('%Y-%m-%d %H:%M'))

    class Meta:
        ordering = ('-active', 'site_sport', '-created')
        verbose_name = 'Player Pool'


class Salary(models.Model):
    """
    This model maintains a salary amount for a given player associated with a
    salary pool.
    """
    created = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='When was this salary last updated?',
        null=True,
        blank=True,
    )

    pool = models.ForeignKey(
        Pool,
        null=False
    )

    amount = models.PositiveIntegerField(
        null=False,
        verbose_name='Salary'
    )

    # new field to store the salary without ownership % adjustments
    amount_unadjusted = models.PositiveIntegerField(
        null=False,
        default=0,
        verbose_name='Salary Pre-Ownership Adjustments'
    )

    flagged = models.BooleanField(
        default=False,
        null=False
    )

    salary_locked = models.BooleanField(
        default=False,
        null=False,
        verbose_name="Locked",
        help_text=(
            'Lock this salary until the next draftgroup is created. This prevents the salary'
            ' you see from being overridden by a stats.com projection update'),
    )

    primary_roster = models.ForeignKey(
        RosterSpot,
        null=False,
        verbose_name='Position'
    )

    fppg = models.FloatField(
        default=0.0,
        verbose_name='STATS Projection',
        help_text=''
    )

    fppg_pos_weighted = models.FloatField(
        default=0.0,
        verbose_name='STATS Projection'
    )

    avg_fppg_for_position = models.FloatField(
        default=0.0,
        verbose_name='Avg Proj for Position'
    )

    # this column no longer has a use, when using stats.com projections.
    num_games_included = models.IntegerField(
        default=0,
        null=False,
        verbose_name='Num Games Included'
    )

    # the GFK to the Player
    # This is a <sport>.models.Player instance.
    player_type = models.ForeignKey(ContentType)
    player_id = models.PositiveIntegerField()
    player = GenericForeignKey('player_type', 'player_id')

    # field for the ownership percentage value which may
    # be used in postprocessing to adjust salary
    ownership_percentage = models.FloatField(
        null=True,
        default=10.0
    )

    # new fields to compare DK & FD salaries (if they exist, for the last generation)
    sal_dk = models.FloatField(
        null=True,
        blank=True,
        verbose_name='DK Salary'
    )

    sal_fd = models.FloatField(
        null=True,
        blank=True,
        verbose_name='FD Salary'
    )

    random_adjust_amount = models.FloatField(
        null=False,
        default=0.0,
        help_text='the amount of ($) salary +/- applied before final rounding.'
    )

    def __str__(self):
        return "<Salary> player_id: %s | amount: %s | fppg: %s | pool: %s" % (
            self.player_id, self.amount, self.fppg, self.pool)

    class Meta:
        ordering = ('primary_roster', '-amount')
        verbose_name = 'Player'
