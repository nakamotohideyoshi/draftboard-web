from django.db import models

class Payout(models.Model):
    created = models.DateTimeField( auto_now_add=True)
    transaction = models.ForeignKey("transaction.models.Transaction",
                                    null=False)
    contest = models.ForeignKey("contest.models.Contest")
    entry = models.ForeignKey("contest.models.Entry")



