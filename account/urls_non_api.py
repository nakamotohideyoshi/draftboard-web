from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
# from debreach.decorators import csrf_protect, csrf_decrypt
from account.views import (
    login,
    RegisterView,
    schema_view,
    ExclusionFormView,
    AccessSubdomainsTemplateView,
    ConfirmUserEmailView,
    LimitsFormView,
)


urlpatterns = [
    # django auth views we choose to have
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', auth_views.logout_then_login),
    url(r'^confirm-email/(?P<uid>.+)/$', ConfirmUserEmailView.as_view(), name='join-confirmation'),
    url(r'^password/reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password/reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^register/', RegisterView.as_view(), name='register'),

    url(r'^admin/', include(admin.site.urls)),

    # frontend templates, will eventually be separated out
    url(r'', include('frontend.urls', namespace='frontend')),
    url(r'^self-exclusion/$', ExclusionFormView.as_view(), name='self-exclusion'),
    url(r'^access_subdomains/$', AccessSubdomainsTemplateView.as_view(), name='site-subdomains-access'),
    # TODO swagger docs should not be on production
    url(r'^docs/', schema_view),
    url(r'^access_subdomains/$', AccessSubdomainsTemplateView.as_view(), name='site-subdomains-access'),
    url(r'^limits/$', LimitsFormView.as_view(), name='user-limits'),
]
