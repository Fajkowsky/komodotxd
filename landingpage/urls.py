from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'landingpage.views.index', name='index'),
    url(r'^404/$', 'landingpage.views.error', name='error'),
    url(r'^thanks/$', 'landingpage.views.thanks', name='thanks'),
    url(r'^confirmation/(?P<userid>[a-z0-9]+)$', 'landingpage.views.confirmation', name='confirmation'),
    url(r'^account/$', 'landingpage.views.account', name='account'),
)
