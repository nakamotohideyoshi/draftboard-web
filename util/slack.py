#
# utils/slack.py

import requests
import json

# exceptions
class InvalidIdentifierException(Exception): pass

class InvalidChannelException(Exception): pass

class SportSchedulerWebhookException(Exception): pass

class Webhook(object):

    # just some interesting icons available...
    ICON_NBA = 'basketball'
    ICON_NFL = 'football'
    ICON_MLB = 'baseball'
    ICON_NHL = 'ice_hockey_stick_and_puck'

    # list of icons
    icons = {
        'nba' : ICON_NBA,
        'nfl' : ICON_NFL,
        'mlb' : ICON_MLB,
        'nhl' : ICON_NHL,
    }

    #
    # exceptions


    #
    # the base url that we will use for posting slack webhooks
    base_url    = 'https://hooks.slack.com/services'

    #
    # *must be set in child class*
    # ex: 'T03UVUNP8/B0K6GUFE3/CNop5c62QB6LFTNOmccnHCzT'
    identifier  = None

    #
    # *must be set in child class*
    # ex: '#scheduler-logs'.
    channel     = None

    # may be set in child class
    # ex: 'webhookbot'   (that is the default)
    username    = 'server'

    def __init__(self):

        self.icon       = 'spiral_calendar_pad' # a little clock icon at 7pm on the dial
        self.username   = 'server-webhook'

        self.session    = requests.Session()
        self.r          = None # request

    def send(self, text, attachments=None, verbose=True):
        self.data = {
            'channel'   : self.channel,
            'username'  : self.username,
            'icon_emoji': ':%s:' % self.icon,
            'text'      : text,
        }

        if attachments is not None:
            self.data['attachments'] = attachments

        url = '%s/%s' % (self.base_url, self.identifier)
        r = self.session.post( url, json.dumps(self.data) )
        print(str(r.status_code), r.text)
        return r

class WebhookContestScheduler(Webhook):

    identifier = 'T03UVUNP8/B0K6GUFE3/CNop5c62QB6LFTNOmccnHCzT'

    def __init__(self, sport):
        super().__init__()
        self.sport      = sport
        self.username   = '%s-scheduler' % self.sport
        self.icon       = self.icons.get(sport)

    def send(self, text, existing, created, total, warn=False, err_msg=None):

        if err_msg is not None:
            attachments = [
                {
                    "color"  : "#ff3333",   # red
                    'fields' : [
                        {
                            "title": "Issue",
                            "value": '%s' % err_msg,
                            "short": False
                        }
                    ]
                }
            ]
        elif total == 0:
            attachments = None
        else:
            attachments = [
                {
                    "color"  : "#333333",   # very dark
                    'fields' : [
                        {
                            "title": "Contests",
                            "value": "%s of %s" % (str(existing+created), str(total)),
                            "short": True
                        }
                    ]
                }
            ]

            if created > 0:
                attachments.append(
                    {
                        "color"  : "#33ff33",   # green
                        'fields' : [
                            {
                                "title": "Newly Created",
                                "value": "%s" % (str(created)),
                                "short": True
                            }
                        ]
                    }
                )

        if warn:
            if attachments is None:
                attachments = []
            attachments.append(
                {
                        "color"  : "#ffff33",   # yellow
                        'fields' : [
                            {
                                "title": "Investigate",
                                "value": 'There are not enough games for this schedule to '
                                         'run on the planned day. It might have scheduled '
                                         'games for the following day, or failed. Please check.',
                                "short": False
                            }
                        ]
                    }
            )

        # call super
        super().send( text, attachments=attachments )



    @staticmethod
    def get_for_sport(sport):
        if sport == 'nba': return NbaSchedulerWebhook()
        elif sport == 'nfl': return NflSchedulerWebhook()
        elif sport == 'mlb': return MlbSchedulerWebhook()
        elif sport == 'nhl': return NhlSchedulerWebhook()
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