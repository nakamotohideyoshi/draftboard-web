#
# prize/urls.py

from django.conf.urls import patterns
from prize.views import CreatePrizeStructureView, PrizeGeneratorView, \
                        TicketPrizeStructureCreatorView, \
                        FlatCashPrizeStructureCreatorView, \
                        PrizeStructureAPIView

urlpatterns = patterns(
    '',

    # deprecated
    (r'^create-prize-structure/$', CreatePrizeStructureView.as_view()),

    # cash prize structure creator view
    (r'^generator/$', PrizeGeneratorView.as_view()),

    # ticket prize structure creator view
    (r'^ticket/$', TicketPrizeStructureCreatorView.as_view()),

    # flat cash prize structure (for 50-50's and triple ups)
    (r'^flat/$', FlatCashPrizeStructureCreatorView.as_view()),

    #
    (r'^(?P<id>[0-9]+)/$', PrizeStructureAPIView.as_view()),
)
