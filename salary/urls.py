#
# urls.py

from .views import (
    PoolGeneratorView,
    ConfigAPIView,
    ConfigRetrieveAPIView,
    SalaryPlayers2CsvAPIView,
)
from django.conf.urls import url

urlpatterns = [

    url(r'^pool-generator/$', PoolGeneratorView.as_view()),

    url(r'^config/$', ConfigAPIView.as_view()),

    url(r'^config/retrieve/(?P<pk>[0-9]+)/$', ConfigRetrieveAPIView.as_view()),

    # download a salary pool's players in csv format
    url(r'^export-pool-csv/(?P<salary_pool_id>[0-9]+)/$', SalaryPlayers2CsvAPIView.as_view()),

]
