#
# contest/classes.py

from .models import Contest
from sports.models import SiteSport
from dataden.util.timestamp import DfsDateTimeUtil
from datetime import datetime
from datetime import timedelta
from datetime import time
from django.utils import timezone
from sports.classes import SiteSportManager as SSM
from ticket.classes import TicketManager
from ticket.models import TicketAmount
from contest.models import Contest
from prize.classes import TicketPrizeStructureCreator

class AbstractContestCreator(object):

    def __init__(self, name, sport, prize_structure):
        self.name               = None
        self.site_sport         = None
        self.prize_structure    = None
        self.start              = None  # start of the contest
        self.end                = None  # live games must start before this datetime

    def create(self):
        """
        Validate all the internal fields which will make this contest.
        Then create the underlying model and return it.
        """
        c =  Contest(name=self.name,
                     site_sport=self.site_sport,
                     prize_structure=self.prize_structure,
                     start=self.start,
                     end=self.end)
        c.save()
        return c

class ContestCreator(AbstractContestCreator):

    def __init__(self, name, sport, prize_structure, start, end):
        self.name               = name
        self.site_sport         = SiteSport.objects.get( name=sport )
        self.prize_structure    = prize_structure
        self.start              = start     # start of the contest
        self.end                = end       # live games must start before this datetime

class Dummy(object):
    """
    Create for the current day that starts in the evening
    """

    DEFAULT_NAME = 'dummy-contest'

    @staticmethod
    def create(sport='nfl'):

        TicketManager.create_default_ticket_amounts()
        ticket_amount = TicketAmount.objects.all()[0]
        #ticket_amount.amount
        ticket_prize_creator = TicketPrizeStructureCreator(ticket_value=5.00,
                                    number_of_prizes=1, name='contest-dummy-prize-structure')
        prize_structure = ticket_prize_creator.save()
        #prize_structure.name
        now = timezone.now()
        start = DfsDateTimeUtil.create( now.date(), time(23,0) )
        end = DfsDateTimeUtil.create( now.date() + timedelta(days=1), time(0,0) )
        creator = ContestCreator( name=Dummy.DEFAULT_NAME,
                                  sport=sport,
                                  prize_structure=prize_structure,
                                  start=start, end=end )
        contest = creator.create()
        print('created new dummy contest with pk:', contest.pk)
        return contest

