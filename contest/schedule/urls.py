#
# schedule/contest/urls.py

from django.conf.urls import patterns
from django.conf.urls import url
from contest.schedule.views import TemplateContestCreate, TemplateContestUpdate

urlpatterns = patterns( '',

    #
    # the add and view forms are custom for the TemplateContest objects
    url(r'^add/$', TemplateContestCreate.as_view(), name='templatecontest_add'),
    url(r'^(?P<pk>[0-9]+)/$', TemplateContestUpdate.as_view(), name='templatecontest-detail'),

)

