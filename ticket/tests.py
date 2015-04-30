from test.classes import AbstractTest
from .classes import TicketManager
from .models import TicketAmount
import ticket.models
import mysite.exceptions
class TicketManagerTest(AbstractTest):
    def setUp(self):
        self.user           = self.get_admin_user()
        #
        # Creates a ticket amount for testing
        self.good_amount    = 5.50
        self.bad_amount     = 5.21
        ta = TicketAmount()
        ta.amount = self.good_amount
        ta.save()

    def test_initialization(self):
        self.assertIsNotNone(TicketManager(self.user))

    def test_good_deposit(self):
        tm = TicketManager(self.user)
        tm.deposit(self.good_amount)
        self.assertEquals(self.good_amount, tm.ticket.amount.amount)
    def test_bad_deposit(self):
        tm = TicketManager(self.user)
        self.assertRaises(
            ticket.models.TicketAmount.DoesNotExist,
            lambda:tm.deposit(self.bad_amount)
        )

    def test_negative_deposit(self):
        tm = TicketManager(self.user)
        self.assertRaises(
            mysite.exceptions.AmountNegativeException,
            lambda:tm.deposit(-1.10)
        )
    def test_zero_deposit(self):
        tm = TicketManager(self.user)
        self.assertRaises(
            mysite.exceptions.AmountZeroException,
            lambda:tm.deposit(0)
        )

    def test_bad_transaction_deposit(self):
        tm = TicketManager(self.user)
        self.assertRaises(
            mysite.exceptions.IncorrectVariableTypeException,
            lambda:tm.deposit(self.good_amount, 1 )
        )