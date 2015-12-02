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
import optimal_payments.urls


from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

# def index(self, *args, **kwargs):
#      return admin.site.__class__.index(self, extra_context={'title':'customized title'}, *args, **kwargs)
# admin.site.index = index.__get__(admin.site, admin.site.__class__)

urlpatterns = [
    # experimental
    url(r'^admin/', include('smuggler.urls')),  # before admin url patterns!

    url(r'^admin/',         include(admin.site.urls)),

    url(r'^api/payments/',      include(optimal_payments.urls)),
    url(r'^api/account/',       include(account.urls)),
    url(r'^api/cash/',          include(cash.urls)),
    url(r'^api/contest/',       include(contest.urls)),
    url(r'^api/draft-group/',   include(draftgroup.urls)),
    url(r'^api/lineup/',        include(lineup.urls)),
    url(r'^api/ticket/',        include(ticket.urls)),
    url(r'^api/prize/',         include(prize.urls)),
    url(r'^api/salary/',        include(salary.urls)),
    url(r'^api/sports/',        include(sports.urls)),

    # TEMP to show pusher
    url(r'^push/', include(push.urls, namespace='push')),

    url(r'', include('frontend.urls', namespace='frontend')),

    #
    # this came with rest_framework
    url(r'^', include(router.urls)),

    #
    # this came with rest_framework
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # JWT support.
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),

    url(r'^account/', include(account.urls)),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ]
