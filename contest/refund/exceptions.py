class ContestRefundInProgressException(Exception):
    def __init__(self, contest_id):
        super().__init__(
            "The contest[" + str(contest_id) + "] is currently being refunded. Check again later.")


class UnmatchedEntryRefundInProgressException(Exception):
    def __init__(self, entry):
        super().__init__(
            "Unmatched entry is currently being refunded. Check again later. Entry: %s" % entry)


class UnmatchedEntryIsInContest(Exception):
    def __init__(self, entry):
        super().__init__(("An entry that is in a contest was attempted to be refunded as "
                          "if it were unmatched. Entry: %s") % entry)


class EntryCanNotBeUnregisteredException(Exception): pass


class ForbiddenUserException(Exception): pass
