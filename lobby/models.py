#
# lobby/models.py

from django.db import models

class AbstractBanner(models.Model):

    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)

    internal_description = models.CharField(max_length=2048, null=False, default='',
                            help_text='PRIVATE description of what this banner is for. should not displayed on the front end')
    start_time  = models.DateTimeField(null=False,
                    help_text='do not display the banner before the start time')
    end_time    = models.DateTimeField(null=False,
                    help_text='all good things must come to an end. and you need to specify the time when this banner should no longer be displayed.')
    image_url   = models.URLField(null=True,
                    help_text='a public link to the image for this banner')
    links_to    = models.URLField(null=True,
                    help_text='if you want the banner to be clickable, then you should add a link here')

    priority    = models.IntegerField(default=1, null=False,
                    help_text='1 = highest priority, 1 > 2 > 3... etc...')
    class Meta:

        abstract = True

        ordering = ['priority']

class PromotionBanner( AbstractBanner ):

    class Meta:
        abstract = False

class ContestBanner( AbstractBanner ):

    contest = models.ForeignKey('contest.Contest', null=True, blank=True)