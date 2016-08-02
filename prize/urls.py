#
# prize/urls.py

from django.conf.urls import url
from prize.views import CreatePrizeStructureView, PrizeGeneratorView, \
    TicketPrizeStructureCreatorView, \
    FlatCashPrizeStructureCreatorView, \
    PrizeStructureAPIView

urlpatterns = [
    # deprecated
    url(r'^create-prize-structure/$', CreatePrizeStructureView.as_view()),

    # cash prize structure creator view
    url(r'^generator/$', PrizeGeneratorView.as_view()),

    # ticket prize structure creator view
    url(r'^ticket/$', TicketPrizeStructureCreatorView.as_view()),

    # flat cash prize structure (for 50-50's and triple ups)
    url(r'^flat/$', FlatCashPrizeStructureCreatorView.as_view()),

    #
    url(r'^(?P<id>[0-9]+)/$', PrizeStructureAPIView.as_view()),
]
