#
# prize/urls.py

from django.conf.urls import patterns
from django.views.generic import TemplateView

# from account.views import RegisterAccountView, UserView,InformationView
# urlpatterns = patterns('',
#     (r'^register/$', RegisterAccountView.as_view()),
#     (r'^information/$', InformationView.as_view()),
#     (r'^settings/$', UserView.as_view()),
#
# )

from prize.views import CreatePrizeStructureView, PrizeGeneratorView

urlpatterns = patterns(
    '',

    #
    (r'^create-prize-structure/$', CreatePrizeStructureView.as_view()),

    #
    (r'^generator/$', PrizeGeneratorView.as_view()),

)