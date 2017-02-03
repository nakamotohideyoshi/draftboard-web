# If a user has already succesfully been paid, and we're trying to pay out again.
class PayoutAlreadyPaid(Exception):
    pass

# General Paypal Payout Error.
class PayoutError(Exception):
    pass
