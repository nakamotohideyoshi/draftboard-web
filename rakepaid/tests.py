#
# rakepaid/tests.py

from mysite.exceptions import AmountZeroException
from test.classes import AbstractTest
from .classes import RakepaidTransaction, LoyaltyStatusManager
from .models import LoyaltyStatus, PlayerTier

class PlayerTierTest(AbstractTest):
    """
    create a basic contest, and use the BuyinManager to buy into it.
    """

    def setUp(self):
        self.user           = self.get_basic_user()
        self.statuses       = LoyaltyStatus.objects.all().order_by('rank')
        size = len(self.statuses)
        if size < 2:
            raise Exception('there are less than two "VIP" statuses ... something is not initialized')
        self.lowest_status  = self.statuses[ :1 ]           # get the first item in the queryset
        #self.highest_status = self.statuses[ size-1:size ]  # get the last object (the highest rank)
        manager = LoyaltyStatusManager( self.user )
        manager.update()

    def __get_player_tier(self, user):
        return PlayerTier.objects.get( user=user )

    def test_all(self):
        amount_already_added = 0
        for status in self.statuses:
            # create a rakepaid transaction to give the user
            # the exact amount where their tier should roll into the next one!
            rpt = RakepaidTransaction(self.user)
            add_amount = status.thirty_day_avg - amount_already_added
            try:
                rpt.deposit( add_amount )
            except AmountZeroException:
                pass # ignore the exception that happens from adding 0

            amount_already_added += add_amount

            # now call update for this user, and validate they are that tier
            manager = LoyaltyStatusManager( self.user )
            manager.update()
            print( 'manager.player_tier.status', str(manager.player_tier.status), ' == (?) ', str(status))
            self.assertEqual( manager.player_tier.status, status )
