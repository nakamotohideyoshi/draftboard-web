from enum import Enum

class WithdrawStatusConstants(Enum):
    """
    Constants for the :class:`cash.withdraw.models.WithdrawStatus`.
    """
    Pending = 1
    Processed = 2
    CancelledAdminDefault = 3


    def getJSON():

        arr = [
                  {
                    "pk": WithdrawStatusConstants.Pending.value,
                    "fields":
                      {
                        "category": "Pending",
                        "description": "Pending Cash Withdrawal",
                        "name": "Pending"
                      }
                  },
                  {
                    "pk": WithdrawStatusConstants.Processed.value,
                    "fields":
                      {
                        "category": "Processed",
                        "description": "Processed",
                        "name": "Processed"
                      }
                  },
                  {
                    "pk": WithdrawStatusConstants.CancelledAdminDefault.value,
                    "fields":
                      {
                        "category": "Cancelled",
                        "description": "Cancelled by the administrator.",
                        "name": "CancelledAdminDefault"
                      }
                  }
            ]
        return arr