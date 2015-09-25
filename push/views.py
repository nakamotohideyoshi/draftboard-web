from pusher import Pusher

from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic.base import View


# referenced http://pusher.com/docs/server_api_guide#/lang=python
class PusherSendView(View):
    """
    Sends an email to devs with log information for the video player
    """
    def get(self, request, *args, **kwargs):
        p = Pusher(
          app_id=settings.PUSHER_APP_ID,
          key=settings.PUSHER_KEY,
          secret=settings.PUSHER_SECRET
        )
        p['test_channel'].trigger('my_event', {'message': 'hello world'})

        return super(PusherSendView, self).get(request, *args, **kwargs)


class PusherReceiverTemplateView(TemplateView):
    template_name = 'pusher/push_receive.html'


    def get_context_data(self, **kwargs):
        context = super(PusherReceiverTemplateView, self).get_context_data(**kwargs)
        context['PUSHER_KEY'] = settings.PUSHER_KEY

        return context
