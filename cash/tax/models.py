from django.db import models
from django.contrib.auth.models import User


class Tax( models.Model ):
    """
    This class keeps track of all
    """
    user            = models.ForeignKey( User )
    tax_identifier  = models.CharField( max_length=9, null=False )
    created         = models.DateTimeField( auto_now_add=True, null=True)

    class Meta:
        unique_together = ('tax_identifier', 'user')


