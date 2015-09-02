#
# replayer/models.py

from django.db import models

class Replay(models.Model):
    created     = models.DateTimeField(auto_now_add=True, null=False)
    name        = models.CharField(max_length=256, null=False)

    start       = models.DateTimeField(null=False)
    end         = models.DateTimeField(null=True)    # it has not ended yet.

class Update(models.Model):

    # the timestamp when this update happened in actual real-time
    ts = models.DateTimeField(null=False)

    # the namespace this Update was triggered from -- the dot separated
    # mongo db.colletion. for example, this is a namespace: "nba.game"
    ns  = models.CharField(max_length=64, null=False)

    # the dictionary object dumped to a string, which contains the update data
    o   = models.CharField(max_length=8192, null=False)