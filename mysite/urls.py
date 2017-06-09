from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles import views
from rest_framework_jwt import views as jwt_views

import account.urls
import cash.urls
import contest.urls
import draftgroup.urls
import lineup.urls
import prize.urls
import salary.urls
import sports.urls
import ticket.urls
from .views import AppConfigView

# Set admin titles.
admin.site.site_header = "Draftboard Admin"

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # api
    url(r'^api/account/', include(account.urls)),
    url(r'^api/cash/', include(cash.urls)),
    url(r'^api/contest/', include(contest.urls)),
    url(r'^api/draft-group/', include(draftgroup.urls)),
    url(r'^api/lobby/', include('lobby.urls')),
    url(r'^api/lineup/', include(lineup.urls)),
    url(r'^api/ticket/', include(ticket.urls)),
    url(r'^api/prize/', include(prize.urls)),
    url(r'^api/push/', include('push.urls')),
    url(r'^api/replayer/', include('replayer.urls')),
    url(r'^api/salary/', include(salary.urls)),
    url(r'^api/sports/', include(sports.urls)),
    url(r'^api/config/', AppConfigView.as_view()),
    # this came with rest_framework
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # JWT support.
    url(r'^api-token-auth/', jwt_views.obtain_jwt_token),
    url(r'^api-token-refresh/', jwt_views.refresh_jwt_token),
    url(r'^api-token-verify/', jwt_views.verify_jwt_token),

    # TEMP to show pusher
    # url(r'^push/', include(push.urls, namespace='push')),

    # All non-API urls. (these serve up html templates)
    url(r'^', include('account.urls_non_api')),
    # Admin
    url(r'^thinking_face/', admin.site.urls, name="admin"),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ]
