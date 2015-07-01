#
# contest/models.py

from django.db import models
from sports.classes import SiteSportManager

class Contest(models.Model):
    """
    Represents all the settings, and statuses of a Contest.
    """

    SCHEDULED = 'SCH'
    INPROGRESS = 'INP'
    COMPLETED = 'CMP'
    CLOSED = 'CLS'
    STATUS = (
        (SCHEDULED, 'Scheduled'), # initial state
        (INPROGRESS, 'In Progress'), # game is locked, no new entries
        (COMPLETED, 'Completed'), # all scores are completed
        (CLOSED, 'Closed'), # game is paid out, last status
    )
    created = models.DateTimeField(auto_now_add=True)

    site_sport = models.ForeignKey('sports.SiteSport', null=False)

    name = models.CharField(default="",
                            null=False,
                            help_text= "The plain text name of the Contest",
                                                           verbose_name="Name",
                                                           max_length=64)
    prize_structure = models.ForeignKey('prize.PrizeStructure',
                              null=False)
    status = models.CharField(max_length=3,
                              choices=STATUS,
                              default=SCHEDULED,
                              null=False)

    # start & today_only/end determine the range of time,
    # in between which live sporting events will be included
    # and players from them can be drafted
    start       = models.DateTimeField(null=False,
                    verbose_name='The time this contest will start!',
                    help_text='the start should coincide with the start of a real-life game.')
    today_only  = models.BooleanField(default=True, null=False)
    end         = models.DateTimeField(null=False,
                    verbose_name='the time, after which real-life games will not be included in this contest',
                    help_text='this field is overridden if the TodayOnly box is enabled')

    # set the pool of players this contest can draft from
    draft_group = models.ForeignKey('draftgroup.DraftGroup', null=True,
                    verbose_name='DraftGroup',
                    help_text='the pool of draftable players and their salaries, for the games this contest includes.' )

    def update_status(self):
        """
        Updates the status for the contest based on the player pool's game
        statuses. Once the first game has started for a contest, the status
        should be turned to In Progress. Once the games are completed and
        the stats for the game are set to "closed" in sports radar feeds, the
        game should be set to completed. At this point the payout task
        can be initiated and once all of the places have been paid out, the
        status can be set to closed.
        """
        pass

    def __get_game_model(self):
        ssm = SiteSportManager()
        return ssm.get_game_class(self.site_sport)

    def games(self):
        game_model = self.__get_game_model()
        return game_model.objects.filter( start__gte=self.start, start__lt=self.end )

class Entry(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    contest = models.ForeignKey(Contest, null=False)
    lineup = models.ForeignKey("lineup.Lineup")
