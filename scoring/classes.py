#
# scoring/classes.py

from scoring.models import ScoreSystem, StatValue

class AbstractScoreSystem(object):

    score_system    = None
    stat_values     = None

    def __init__(self):
        self.stat_values = self.get_stat_values()
        self.__validate()

    def __validate(self):
        """

        :return:
        """
        if self.score_system is None:
            raise Exception('"score_system" cant be None')
        if self.stat_values is None:
            raise Exception('"stat_values" cant be None')
        if len(self.stat_values) == 0:
            raise Exception('"stat_values" list cant be empty')

    def get_stat_values(self):
        """
        from the db, load the StatValue objects associated with this scoring system
        :return:
        """
        self.stat_values = StatValue.objects.filter(score_system=self.score_system)

    def format_stat(self, real_stat, stat_value):
        """
        format real_stat to a string in the format the stat_value defines for it.

        ie: format the models "home_run" field value to "2HR"  -- just an example
        """
        return 'format_stat() unimplemented for: real_stat[%s] stat_value[%s]' % \
                                                    (str(real_stat), str(stat_value))

class NbaSalaryScoreSystem(AbstractScoreSystem):
    """
    defines the NBA Salary Draft scoring metrics
    """
    def __init__(self):
        self.score_system = ScoreSystem.objects.get(sport='nba', name='salary')

        #
        # call super last - it will perform validation and ensure proper setup
        super().__init__()

class MlbSalaryScoreSystem(AbstractScoreSystem):
    """
    defines the MLB Salary draft scoring metrics
    """
    def __init__(self):
        self.score_system = ScoreSystem.objects.get(sport='mlb', name='salary')

        #
        # call super last!
        super().__init__()
