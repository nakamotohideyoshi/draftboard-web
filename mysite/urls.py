from django.conf.urls import patterns
from django.contrib import admin

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

    url(r'^admin/', include(admin.site.urls)),

    url(r'^account/', include(account.urls)),
    url(r'^cash/', include(cash.urls)),
    url(r'^contest/', include(contest.urls)),
    url(r'^draft-group/', include(draftgroup.urls)),
    url(r'^lineup/',      include(lineup.urls)),
    url(r'^ticket/', include(ticket.urls)),
    url(r'^prize/',  include(prize.urls)),
    url(r'^salary/', include(salary.urls)),
    url(r'^sports/', include(sports.urls)),

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
]

# urlpatterns = patterns('',
#     # Examples:
#     # url(r'^$', 'mysite.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),
#
#     url(r'^admin/', include(admin.site.urls)),
#
#     url(r'^account/', include(account.urls)),
# )
