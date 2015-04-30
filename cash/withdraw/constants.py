from enum import Enum

class WithdrawStatusConstants(Enum):
    """
    Constants for the :class:`cash.withdraw.models.WithdrawStatus`.
    """
    Pending                 = 1     # initial state of a withdraw request. ie: user just submitted withdraw request
    Processed               = 2     # the final "success" state of a withdraw which has fully paid out
    CancelledAdminDefault   = 3     # the withdraw request was declined
    Processing              = 4     # indicates payout has been confirmed, and awaiting final confirmation


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
                  },
                  {
                    "pk": WithdrawStatusConstants.Processing.value,
                    "fields":
                      {
                        "category": "Processing",
                        "description": "Awaiting final confirmation payout completed successfully.",
                        "name": "Processing"
                      }
                  }
            ]
        return arr