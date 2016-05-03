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
    created                             = models.DateTimeField( auto_now_add=True)

    name                                = models.CharField(default="",
                                                           null=False,
                                                           help_text= "The plain text name of the configuration",
                                                           verbose_name="Name",
                                                           max_length=64)
    days_since_last_game_flag           = models.PositiveIntegerField(null = False,
                                                                      help_text="Flag the player if X days since last game played",
                                                                      verbose_name="Days Since Last Game Flag")
    min_games_flag                      = models.PositiveIntegerField(null = False,
                                                                      help_text="Flag the player if X games have not been played",
                                                                      verbose_name="Min Games Flag")
    min_player_salary                   = models.PositiveIntegerField(null = False,
                                                                      help_text="The minimum salary a player can be worth.",
                                                                      verbose_name="Min Player Salary")
    max_team_salary                     = models.PositiveIntegerField(null = False,
                                                                      help_text="The total team salary for drafting",
                                                                      verbose_name="Team Salary")
    min_avg_fppg_allowed_for_avg_calc   = models.FloatField(null = False,
                                                            default=0.0,
                                                            help_text="The minimum fppg allowed for a player's stats to be used to calculate position averages.",
                                                            verbose_name="Min FPPG Allowed for Avg Calc")




    trailing_games                      = models.PositiveIntegerField(null = False,
                                                                      help_text="The total number of games considered in the trailing weight section.",
                                                                      verbose_name="Trailing Games")




    def __str__(self):
        return '%s: %s' % (str(self.id), self.name)

    class Meta:
        verbose_name = 'Algorithm'



class TrailingGameWeight(models.Model):
    """
    The weights of the scores for each tier of trailing games
    """
    salary                      = models.ForeignKey( SalaryConfig, null = False, related_name='trailing_game_weights')
    through                     = models.PositiveIntegerField(null = False)
    weight                      = models.FloatField(null = False,
                                                    help_text="Multiplier")


    class Meta:
        unique_together = ( 'salary', 'through' )
        ordering = ('through',)

class Pool(models.Model):
    """
    Creating a Pool with active=True will mark the existing active pool False!

    This model keeps track of all the player pools for all the sports and also
    maintains the active player pool status. Only one pool per site_sport can be
    active.
    """
    created                     = models.DateTimeField( auto_now_add=True )
    site_sport                  = models.ForeignKey( sports.models.SiteSport, null = False )
    active                      = models.BooleanField( null = False, default=False )
    salary_config               = models.ForeignKey( SalaryConfig, null = False )
    generate_salary_task_id     = models.CharField(default=None,
                                                   null=True,
                                                   verbose_name="Generating Salary",
                                                   max_length=255)

    #
    # fields for factoring in ownership percentages.
    ownership_threshold_low_cutoff  = models.FloatField(null=True, default=10.0)
    low_cutoff_increment = models.FloatField(null=True, default=1.0)
    ownership_threshold_high_cutoff = models.FloatField(null=True, default=30.0)
    high_cutoff_increment = models.FloatField(null=True, default=1.0)

    #
    # make sure that only one Pool can be active at a time (for the site_sport)
    def save(self, *args, **kwargs):
        if self.active:
            try:
                temp = Pool.objects.get(active=True, site_sport= self.site_sport)
                if self != temp:
                    temp.active = False
                    temp.save()
            except Pool.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return '%s: active[%s] : %s : %s' % (str(self.id), self.active,
                    str(self.site_sport), self.created.strftime('%Y-%m-%d %H:%M'))

    class Meta:
        ordering        = ('-active', 'site_sport', '-created')
        verbose_name    = 'Player Pool'

class Salary(models.Model):
    """
    This model maintains a salary amount for a given player associated with a
    salary pool.
    """
    created         = models.DateTimeField( auto_now_add=True )
    pool            = models.ForeignKey( Pool, null = False )
    amount          = models.PositiveIntegerField(null=False)
    flagged         = models.BooleanField(default=False, null=False)
    primary_roster  = models.ForeignKey(RosterSpot, null = False)
    fppg            = models.FloatField(default=0.0,
                                        verbose_name='Weighted FPPG')


    # the GFK to the Player
    player_type     = models.ForeignKey(ContentType)
    player_id       = models.PositiveIntegerField()
    player          = GenericForeignKey('player_type',
                                        'player_id')

    #
    # field for the ownership percentage value which may
    # be used in postprocessing to adjust salary
    ownership_percentage = models.FloatField(null=True, default=10.0)

    class Meta:
        ordering = ('primary_roster', '-amount')
        verbose_name = 'Player'