class WithdrawStatusException(Exception):
    def __init__(self, withdraw_pk, withdraw_class):
       super().__init__(\
           "The pk "+withdraw_pk+" for the model :"+withdraw_class+" is no longer pending. This action cannot be performed.")