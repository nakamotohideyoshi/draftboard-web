#
# utils/slack.py

import requests

class Webhook(object):

    #
    # exceptions
    class InvalidIdentifierException(Exception): pass
    class InvalidChannelException(Exception): pass

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
    username    = 'webhookbot'

    def __init__(self):


        self.session = requests.Session()
        self.r = None # request
        self.data = {
            "channel": self.channel,
            "username": "webhookbot",
            "text": "Scheduler.", "icon_emoji": ":ghost:"}

    def send(self, data=None):
        send_data = None
        if data is not None:
            send_data = data
        else:
            send_data = self.data

        url = '%s/%s' % (self.base_url, self.identifier)
        return self.session.post( url, data=send_data )

class WebhookContestScheduler(Webhook):

    identifier = 'T03UVUNP8/B0K6GUFE3/CNop5c62QB6LFTNOmccnHCzT'