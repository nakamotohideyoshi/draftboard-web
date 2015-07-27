class WithdrawRakepaidException(Exception):
    def __init__(self):
        super().__init__(\
           "You cannot withrdraw from the Rakepaid model.")