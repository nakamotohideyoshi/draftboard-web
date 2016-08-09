#
# lobby/urls.py

from django.conf.urls import url
from lobby.views import ContestBannerAPIView

urlpatterns = [

    #
    # get all the contest banners
    url(r'^featured-content/$', ContestBannerAPIView.as_view()),
]
