from django.db import models


class Contest(models.Model):
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
    name = models.CharField(default="",
                            null=False,
                            help_text= "The plain text name of the Contest",
                                                           verbose_name="Name",
                                                           max_length=64)
    prize = models.ForeignKey('prize.models.PrizeStructure',
                              null=False)
    status = models.CharField(max_length=3,
                              choices=STATUS,
                              default=SCHEDULED,
                              null=False)

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


class Entry(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    contest = models.ForeignKey(Contest, null=False)
    lineup = models.ForeignKey("lineup.models.Lineup")
