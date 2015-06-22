import mysite.exceptions
from contest.models import Contest
from django.db.models import Q
class PayoutManager(object):
    """
    Responsible for performing the payouts for all active contests for both
    cash and ticket games.
    """

    def __init__(self):
        pass

    def payout(self, contests=None):
        """
        Takes in an array of contests to payout. If there are not contests passed
        then the payout mechanism will look for all contests who have not been
        paid out yet and pay them out.
        :param contests: an array of :class:`contest.models.Contest` models
        """

        #
        # validation if the contests are passed as an argument
        if contests is not None:
            #
            # validate that contests is an array
            if not issubclass(contests, list):
                raise mysite.exceptions.IncorrectVariableTypeException(
                    type(self).__name__,
                    'contests')

            #
            # validate the contest array is an array of contests
            for contest in contests:
                if not isinstance(contest, Contest):
                    raise mysite.exceptions.IncorrectVariableTypeException(
                        type(self).__name__,
                        'contests')

        #
        # find contests that have not been paid out yet that need
        # to be paid out
        else:
            #
            # gets all the contests that are not set to closed
            contests = Contest.objects.filter(~Q(status=Contest.CLOSED))

            #
            # update the status for all of the contests
            for contest in contests:
                contest.update_status()


            #
            # gets all the contests that are completed
            contests = Contest.objects.filter(status=Contest.COMPLETED)

        #
        # If there are contests left to payout, pay them out.
        for contest in contests:
            self.__payout_contest(contest)



    def __payout_contest(self, contest):
        """
        Method assumes the contest has never been paid out and is ready
        to be paid out. This is why the method is private and should be
        called from a separate method that does the individual error checking.
        """

        #
        # get the prize pool
        pass


