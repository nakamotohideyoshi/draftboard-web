from django.conf.urls import patterns
from django.contrib import admin

import account.urls

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
urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),

    url(r'^account/', include(account.urls)),

    #
    # this came with rest_framework
    url(r'^', include(router.urls)),

    #
    # url includes from django_braintree
    url(r'', include('django_braintree.urls')),

    #
    # this came with rest_framework
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

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
