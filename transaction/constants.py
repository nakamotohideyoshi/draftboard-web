
from enum import Enum

class TransactionTypeConstants(Enum):
    """
    Constants for the :class:`transaction.models.TransactionType`.
    """
    CashWithdrawal = 1
    CashDeposit = 2
