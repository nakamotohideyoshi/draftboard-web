from django.db import models


class ScoreSystem(models.Model):
    sport = models.CharField(max_length=64, null=False, default='')
    name = models.CharField(max_length=64, null=False, default='')
    description = models.CharField(max_length=1024, null=False, default='')

    def __str__(self):
        return '%s | %s' % (self.sport, self.name)

    class Meta:
        unique_together = ('sport', 'name')


class StatPoint(models.Model):
    score_system = models.ForeignKey(ScoreSystem, null=False)
    stat = models.CharField(max_length=32, null=False, default='')
    value = models.FloatField(default=0.0, null=False)

    class Meta:
        unique_together = ('score_system', 'stat')

    def __str__(self):
        return '%s=%s' % (self.stat, self.value)
