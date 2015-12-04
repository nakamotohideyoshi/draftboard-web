#
# lobby/urls.py

from django.conf.urls import patterns
from lobby.views import ContestBannerAPIView

urlpatterns = patterns( '',

    #
    # get all the contest banners
    (r'^banner/contests/$', ContestBannerAPIView.as_view()),

)