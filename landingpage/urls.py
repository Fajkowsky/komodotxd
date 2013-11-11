from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'landingpage.views.index', name='index'),
    url(r'^thanks/$', 'landingpage.views.thanks', name='thanks'),
)
