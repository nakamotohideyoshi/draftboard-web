from django.db import models
from django.contrib.auth.models import User

class Lineup(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    fantasy_points = models.FloatField(default=0.0,
                                       null=False,
                                       blank=True)
    user = models.ForeignKey(User,
                             null=False)
