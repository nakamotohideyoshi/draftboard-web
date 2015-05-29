from django.db import models
from sports.models import SiteSport, Position

class RosterSpot(models.Model):
    """
    Model is responsible for holding the Roster Archtypes and their
    quantity for each sport. For example WR could have 2 spots...
    """
    name        = models.CharField(max_length=64, null=False, default='',
                                   help_text='the roster position spot, i.e. FLEX or WR')
    site_sport  = models.ForeignKey(SiteSport, null=False)
    amount      = models.PositiveIntegerField(default = 0, help_text='the quantity of these spots allowed in a lineup for the sport.', null = False)
    idx         = models.PositiveIntegerField(default = 0, help_text='the order the spot will be displayed to the user.', null = False)
    class Meta:
        unique_together = ('name', 'site_sport')


class RosterSpotPosition(models.Model):
    """
    Model for mapping the many :class:`sports.models.Positions` objects
    to the many :class:`roster.models.RosterSpot` objects.
    """
    roster_spot = models.ForeignKey(RosterSpot, null=False)
    position    = models.ForeignKey(Position, null=False)
    is_primary  = models.BooleanField(null = False, default=False)

    def save(self, *args, **kwargs):
        if self.is_primary:
            try:
                temp = RosterSpotPosition.objects.get(is_primary=True, position= self.position)
                if self != temp:
                    temp.is_primary = False
                    temp.save()
            except RosterSpotPosition.DoesNotExist:
                pass
        super(RosterSpotPosition, self).save(*args, **kwargs)
    class Meta:
        unique_together = ('roster_spot', 'position')

