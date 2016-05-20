#
# mysite/urls.py

from django.conf.urls import patterns
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles import views
import account.urls
import cash.urls
import contest.urls
import draftgroup.urls
import lineup.urls
import ticket.urls
import prize.urls
import salary.urls
import sports.urls
import push.urls
from django.conf.urls import url, include

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [

    url(r'^admin/',         include(admin.site.urls)),

    url(r'^api/account/',       include(account.urls)),
    url(r'^api/cash/',          include(cash.urls)),
    url(r'^api/contest/',       include(contest.urls)),
    url(r'^api/draft-group/',   include(draftgroup.urls)),
    url(r'^api/lobby/',         include('lobby.urls')),
    url(r'^api/lineup/',        include(lineup.urls)),
    url(r'^api/ticket/',        include(ticket.urls)),
    url(r'^api/prize/',         include(prize.urls)),
    url(r'^api/push/',          include('push.urls')),
    url(r'^api/salary/',        include(salary.urls)),
    url(r'^api/sports/',        include(sports.urls)),

    # TEMP to show pusher
    url(r'^push/', include(push.urls, namespace='push')),

    url(r'', include('frontend.urls', namespace='frontend')),

    #
    # this came with rest_framework
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # JWT support.
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^api-token-refresh/', 'rest_framework_jwt.views.refresh_jwt_token'),
    url(r'^api-token-verify/', 'rest_framework_jwt.views.verify_jwt_token'),

    url(r'^', include('account.urls_non_api')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ]
