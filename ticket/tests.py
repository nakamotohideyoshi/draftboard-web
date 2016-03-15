#
# ticket/tests.py

from test.classes import AbstractTest
from .classes import TicketManager
from .models import TicketAmount
import ticket.models
import mysite.exceptions
from .exceptions import (
    InvalidTicketAmountException,
    TicketAlreadyUsedException,
    UserDoesNotHaveTicketException,
)

class TicketManagerTest(AbstractTest):

    def setUp(self):
        self.user = self.get_admin_user()
        #
        # Creates a ticket amount for testing
        self.good_amount    = 5.50
        self.bad_amount     = 5.21
        ta = TicketAmount()
        ta.amount = self.good_amount
        ta.save()

    def test_initialization(self):
        self.assertIsNotNone(TicketManager(self.user))

    #---------------------------------------------------------------
    # DEPOSIT TESTS
    #---------------------------------------------------------------

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

    def test_bad_transaction_deposit(self):
        tm = TicketManager(self.user)
        self.assertRaises(
            mysite.exceptions.IncorrectVariableTypeException,
            lambda:tm.deposit(self.good_amount, 1 )
        )

    #---------------------------------------------------------------
    # CONSUME TESTS
    #---------------------------------------------------------------
    def helper_create_deposits(self):
        tm = TicketManager(self.user)
        tm.deposit(self.good_amount)
        return tm

    def test_good_consume(self):
        self.helper_create_deposits()
        tm = TicketManager(self.user)
        tm.consume(self.good_amount)
        self.assertIsNotNone(tm.ticket.consume_transaction)

        htm = self.helper_create_deposits()
        tm = TicketManager(self.user)
        tm.consume(ticket_obj= htm.ticket)
        self.assertIsNotNone(tm.ticket.consume_transaction)

    def test_consume_too_many_args(self):
        htm = self.helper_create_deposits()
        tm = TicketManager(self.user)
        self.assertRaises(mysite.exceptions.TooManyArgumentsException, lambda:tm.consume(self.good_amount,htm.ticket))

    def test_consume_too_little_args(self):
        self.helper_create_deposits()
        tm = TicketManager(self.user)
        self.assertRaises(mysite.exceptions.TooLittleArgumentsException, lambda:tm.consume())

    def test_invalid_amount(self):
        self.helper_create_deposits()
        tm = TicketManager(self.user)
        self.assertRaises(InvalidTicketAmountException, lambda:tm.consume(self.bad_amount))

    def test_user_does_not_have_ticket(self):
        tm = TicketManager(self.user)
        self.assertRaises(UserDoesNotHaveTicketException, lambda:tm.consume(self.good_amount))

    def test_ticket_already_consumed(self):
        htm = self.helper_create_deposits()
        tm = TicketManager(self.user)
        tm.consume(ticket_obj= htm.ticket)
        tm = TicketManager(self.user)
        self.assertRaises(TicketAlreadyUsedException, lambda:  tm.consume(ticket_obj= htm.ticket))

    def test_ticket_incorrect_ticket_object(self):
        self.helper_create_deposits()
        tm = TicketManager(self.user)
        self.assertRaises(mysite.exceptions.IncorrectVariableTypeException, lambda:tm.consume(ticket_obj= 1))

    def test_ticket_incorrect_transaction_object(self):
        self.helper_create_deposits()
        tm = TicketManager(self.user)
        self.assertRaises(mysite.exceptions.IncorrectVariableTypeException, lambda:tm.consume(self.good_amount, transaction_obj = 1))
