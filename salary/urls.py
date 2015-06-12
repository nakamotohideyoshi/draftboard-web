
from .views import PoolGeneratorView, ConfigAPIView, ConfigRetrieveAPIView
from django.conf.urls import patterns

urlpatterns = patterns(
    '',
    (r'^pool-generator/$', PoolGeneratorView.as_view()),
    (r'^config/$', ConfigAPIView.as_view()),
    (r'^config/retrieve/(?P<pk>[0-9]+)/$', ConfigRetrieveAPIView.as_view()),

)
