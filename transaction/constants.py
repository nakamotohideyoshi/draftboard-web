
from enum import Enum

class TransactionTypeConstants(Enum):
    """
    Constants for the :class:`transaction.models.TransactionType`.
    """
    CashWithdraw = 1
    CashDeposit = 2
    AdminCancelWithdraw = 3
    TicketConsume = 4
    TicketDeposit = 5

    FppWithdraw = 6
    FppDeposit = 7

    BonusCashWithdraw   = 8
    BonusCashDeposit    = 9

    # if you add more to this class, remember to add to
    # the migration that puts them in the database!