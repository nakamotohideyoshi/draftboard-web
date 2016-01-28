class ContestRefundInProgressException(Exception):
    def __init__(self, contest_id):
        super().__init__(
           "The contest["+ str(contest_id)+"] is currently being refunded. Check again later.")

class EntryCanNotBeUnregisteredException(Exception): pass