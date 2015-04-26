from . import models
from . import constants
from django.contrib.contenttypes.models import ContentType
# return the number of reviewable withdraw object

# creates context where the models lowercase name
# indexes to the number of pending ones there are
# the return dict is osmething like:
#
#       {'withdraw_model_badges': {'paypalwithdraw': 4, 'checkwithdraw': 4}}
#
def model_badges(request):
    data = {
        'withdraw_model_badges' : {

            # CheckWithdraw pending for review
            ContentType.objects.get_for_model( models.CheckWithdraw ).model :
                models.CheckWithdraw.objects.filter(
                status__pk=constants.WithdrawStatusConstants.Pending.value ).count(),

            # PayPalWithdraw pending for review
            ContentType.objects.get_for_model( models.PayPalWithdraw ).model :
                models.PayPalWithdraw.objects.filter(
                status__pk=constants.WithdrawStatusConstants.Pending.value ).count(),
        }
    }
    #print( data )
    return data