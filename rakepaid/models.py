from django.db import models
from transaction.models import TransactionDetail, Balance

class RakepaidBalance(Balance):
    """
    Implements the :class:`transaction.models.Balance` model.
    """
    pass

class RakepaidTransactionDetail(TransactionDetail):
    """
    Implements the :class:`transaction.models.TransactionDetail` model.
    """
    pass