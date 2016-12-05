import requests
import json
from django.conf import settings
from logging import getLogger

logger = getLogger('util.slack')


# exceptions
class InvalidIdentifierException(Exception):
    pass


class InvalidChannelException(Exception):
    pass


class SportSchedulerWebhookException(Exception):
    pass


class Webhook(object):

    # just some interesting icons available...
    ICON_NBA = 'basketball'
    ICON_NFL = 'football'
    ICON_MLB = 'baseball'
    ICON_NHL = 'ice_hockey_stick_and_puck'

    # list of icons
    icons = {
        'nba': ICON_NBA,
        'nfl': ICON_NFL,
        'mlb': ICON_MLB,
        'nhl': ICON_NHL,
    }

    #
    # exceptions

    #
    # the base url that we will use for posting slack webhooks
    base_url = 'https://hooks.slack.com/services'

    #
    # *must be set in child class*
    # ex: 'T03UVUNP8/B0K6GUFE3/CNop5c62QB6LFTNOmccnHCzT'
    identifier = None

    #
    # *must be set in child class*
    # ex: '#scheduler-logs'.
    channel = None

    # may be set in child class
    # ex: 'webhookbot'   (that is the default)
    username = 'server'

    def __init__(self):

        self.icon = 'spiral_calendar_pad'  # a little clock icon at 7pm on the dial
        self.username = 'server-webhook'

        self.session = requests.Session()
        self.r = None  # request

        self.attachments = []

    def send(self, text, verbose=True):
        self.data = {
            'channel': self.channel,
            'username': self.username,
            'icon_emoji': ':%s:' % self.icon,
            'text': text,
            'attachments': self.attachments,
        }

        url = '%s/%s' % (self.base_url, self.identifier)

        if settings.SLACK_UPDATES is False:
            logger.warn('Not posting to Slack webhook due to settings.SLACK_UPDATES')
            logger.warn('Suppressed: Posting to Slack: %s' % json.dumps(self.data))
            return

        res = self.session.post(url, json.dumps(self.data))
        logger.info('Posting to Slack: %s' % json.dumps(self.data))
        logger.info('Slack response: status code: %s, text: %s ' % (str(res.status_code), res.text))
        return res

    def add_attachment(self, attachment):
        self.attachments.append(attachment.build())


class Attachment(object):

    COLOR_BLACK = '#333333'
    COLOR_RED = '#ff3333'
    COLOR_GREEN = '#33ff33'
    COLOR_YELLOW = '#ffff33'

    def __init__(self, title, value, short=False, color=None):
        self.title = title
        self.value = value
        self.short = short
        self.color = color
        if self.color is None:
            self.color = self.COLOR_BLACK

    def build(self):
        self.data = {
            'color': self.color,
            'fields': [
                {
                    'title': self.title,
                    'value': self.value,
                    'short': self.short,
                }
            ]
        }
        return self.data


class WebhookContestInfo(Webhook):
    """
    use this class for sending non sport-specific notifications to  #contest-updates
    # currently for draftboard: #contest-updates
    # https://hooks.slack.com/services/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
    """
    identifier = 'T02S3E1FD/B3ARUD0V9/S5BmvH6qbrF3SlzyA1R2WAKE'


class WebhookContestScheduler(Webhook):
    """
    use this class for sending notifications to  #contest-updates

    usage:

        from util.slack import WebhookContestScheduler, Attachment
        hook = WebhookContestScheduler('nba')
        a = Attachment('TestTitle','TestValue',color=Attachment.COLOR_RED)
        hook.add_attachment( a )
        hook.send('Main Webhook Text')

    """

    # currently for draftboard: #contest-updates
    # https://hooks.slack.com/services/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
    identifier = 'T02S3E1FD/B3ARUD0V9/S5BmvH6qbrF3SlzyA1R2WAKE'

    def __init__(self, sport):
        super().__init__()
        self.sport = sport
        self.username = '%s-scheduler' % self.sport
        self.icon = self.icons.get(sport)

    @staticmethod
    def get_for_sport(sport):
        if sport == 'nba':
            return NbaSchedulerWebhook()
        elif sport == 'nfl':
            return NflSchedulerWebhook()
        elif sport == 'mlb':
            return MlbSchedulerWebhook()
        elif sport == 'nhl':
            return NhlSchedulerWebhook()
        else:
            raise SportSchedulerWebhookException()


class NbaSchedulerWebhook(WebhookContestScheduler):

    def __init__(self):
        super().__init__('nba')


class NflSchedulerWebhook(WebhookContestScheduler):

    def __init__(self):
        super().__init__('nfl')


class MlbSchedulerWebhook(WebhookContestScheduler):

    def __init__(self):
        super().__init__('mlb')


class NhlSchedulerWebhook(WebhookContestScheduler):

    def __init__(self):
        super().__init__('nhl')
