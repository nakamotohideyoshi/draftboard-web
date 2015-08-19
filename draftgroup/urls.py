#
# draftgroup/urls.py

from django.conf.urls import patterns
from django.conf.urls import url
from draftgroup.views import DraftGroupAPIView

urlpatterns = patterns( '',

    #
    # get the contests for display on the main contest lobby
    (r'^get/$', DraftGroupAPIView.as_view()),

)