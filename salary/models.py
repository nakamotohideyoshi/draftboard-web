from django.db import models
from sports.models import SiteSport
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
class SalaryConfig(models.Model):
    """
    The class that keeps a Salary algorithm for a specified sport
    """
    trailing_games              = models.PositiveIntegerField(null = False)
    days_since_last_game_flag   = models.PositiveIntegerField(null = False)
    min_games_flag              = models.PositiveIntegerField(null = False)
    min_player_salary           = models.PositiveIntegerField(null = False)
    max_team_salary             = models.PositiveIntegerField(null = False)


class TrailingGameWeight(models.Model):
    """
    The weights of the scores for each tier of trailing games
    """
    salary                      = models.ForeignKey( SalaryConfig, null = False)
    through                     = models.PositiveIntegerField(null = False)
    weight                      = models.FloatField(null = False)

    class Meta:
        unique_together = ( 'salary', 'through' )


class Pool(models.Model):
    """
    This model keeps track of all the player pools for all the sports and also
    maintains the active player pool status. Only one pool per site_sport can be
    active. If setting a new pool to active  for a given sport that already has an active
    pool, the old active pool will automatically be deactivated.
    """
    created                     = models.DateTimeField( auto_now_add=True )
    site_sport                  = models.ForeignKey( SiteSport, null = False )
    active                      = models.BooleanField( null = False, default=False )
    salary_config               = models.ForeignKey( SalaryConfig, null = False )

    #
    # overrides the save ot make sure that only one Pool can be active at any
    # given time.
    def save(self, *args, **kwargs):
        if self.active:
            try:
                temp = Pool.objects.get(active=True, site_sport= self.site_sport)
                if self != temp:
                    temp.active = False
                    temp.save()
            except Pool.DoesNotExist:
                pass
        super(Pool, self).save(*args, **kwargs)


class Salary(models.Model):
    """
    This model maintains a salary amount for a given player associated with a
    salary pool.
    """
    created         = models.DateTimeField( auto_now_add=True )
    pool            = models.ForeignKey( Pool, null = False )
    amount          = models.PositiveIntegerField(null=False)
    flagged         = models.BooleanField(default=False, null=False)

    # the GFK to the Player
    player_type     = models.ForeignKey(ContentType,  related_name='%(app_label)s_%(class)s_sport_player')
    player_id       = models.PositiveIntegerField()
    player          = GenericForeignKey('player_type', 'player_id')
