#
# dataden/models.py

from django.db import models

class Game(models.Model):
    created     = models.DateTimeField(auto_now_add=True, null=True)
    updated     = models.DateTimeField(auto_now=True, null=False)

class NbaGame( Game ):
    pass

class MlbGame( Game ):
    pass
