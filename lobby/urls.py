#
# lobby/urls.py

from django.conf.urls import patterns
from lobby.views import ContestBannerAPIView

urlpatterns = patterns( '',

    #
    # get all the contest banners
    (r'^feature/contests/$', ContestBannerAPIView.as_view()),

)