#
# dataden/models.py

from django.db import models

class Trigger(models.Model):
    """
    used by the dataden process monitoring the oplog.
    if enabled, dataden sends signals when new data is found.
    if not enabled, it does not process
    """
    updated     = models.DateTimeField(auto_now=True, null=False)

    #
    enabled     = models.BooleanField(null=False, default=True)

    #
    db          = models.CharField(max_length=128, null=False)
    collection  = models.CharField(max_length=128, null=False)
    parent_api  = models.CharField(max_length=128, null=False)

    #
    @property
    def ns(self):
        return '%s.%s' % (self.db, self.collection)

    def __str__(self):
        if self.enabled:
            enabled_str = 'ENABLED'
        else:
            enabled_str = 'DISABLED'
        return '[%s] %s | %s' % (enabled_str, self.ns, self.parent_api)

    class Meta:
        unique_together = ('db','collection','parent_api')

class LiveStatsCacheConfig(models.Model):
    """
    used by
    """
    updated     = models.DateTimeField(auto_now=True, null=False)

    key_timeout = models.IntegerField(default=1800, null=False)
    timeout_mod = models.IntegerField(default=25, null=False,
                    help_text='the percentage as an integer [25-100], '
                              'of how much to randomize the key_timeout. 25 indicates +/-25%'
                              '  If its set too low the database has a higher likelihood'
                              ' of getting big bursts of insert/updates')

class PbpDebug(models.Model):
    """
    a log table for a standalone script to update a the pbp objects
    as it sees them in real time.
    """
    created     = models.DateTimeField(auto_now_add=True)

    url         = models.CharField(max_length=2048, null=True)
    game_srid   = models.CharField(max_length=128, null=False)
    srid        = models.CharField(max_length=128, null=False)
    description = models.CharField(max_length=1024 * 2, null=True)
    xml_str     = models.CharField(max_length=1024 * 16, null=True)

    class Meta:
        unique_together = ('game_srid','srid')

