from transaction.models import TransactionDetail, Balance



#
# Test models must be created outside of the test
# class
class TransactionDetailChild(TransactionDetail):
    pass

class BalanceChild(Balance):
    pass