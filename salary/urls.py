
from .views import (
    PoolGeneratorView,
    ConfigAPIView,
    ConfigRetrieveAPIView,
    SalaryPlayers2CsvAPIView,
)
from django.conf.urls import patterns

urlpatterns = patterns( '',

    (r'^pool-generator/$', PoolGeneratorView.as_view()),

    (r'^config/$', ConfigAPIView.as_view()),

    (r'^config/retrieve/(?P<pk>[0-9]+)/$', ConfigRetrieveAPIView.as_view()),

    # download a salary pool's players in csv format
    (r'^export-pool-csv/(?P<salary_pool_id>[0-9]+)/$', SalaryPlayers2CsvAPIView.as_view()),

)
