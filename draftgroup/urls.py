#
# draftgroup/urls.py

from django.conf.urls import patterns
from django.conf.urls import url
from draftgroup.views import DraftGroupAPIView

urlpatterns = patterns( '',

    #
    # get the contests for display on the main contest lobby
    (r'^(?P<pk>[0-9]+)/$', DraftGroupAPIView.as_view()),

)
