from enum import Enum

class WithdrawStatusConstants(Enum):
    """
    Constants for the :class:`cash.withdraw.models.WithdrawStatus`.
    """
    Pending = 1
    Processed = 2
    CancelledAdminDefault = 3