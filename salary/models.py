from django.db import models


class SalaryConfig(models.Model):
    """
    The class that keeps a Salary algorithm for a specified sport
    """
    trailing_games              = models.IntegerField()
    days_since_last_game_flag   = models.IntegerField()
    min_games_flag              = models.IntegerField()
    min_player_salary           = models.IntegerField()
    max_team_salary             = models.IntegerField()


class TrailingGameWeight(models.Model):
    """
    The weights of the scores for each tier of trailing games
    """
    salary                      = models.ForeignKey( SalaryConfig )
    through                     = models.IntegerField()
    weight                      = models.FloatField()

    class Meta:
        unique_together = ( 'salary', 'through' )