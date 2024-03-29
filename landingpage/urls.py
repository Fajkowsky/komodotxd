from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
    url(r'^$', 'landingpage.views.index', name='index'),
    url(r'^404/$', 'landingpage.views.error', name='error'),
    url(r'^thanks/$', 'landingpage.views.thanks', name='thanks'),
    url(r'^confirmation/(?P<userid>[a-z0-9]+)$', 'landingpage.views.confirmation', name='confirmation'),
    url(r'^account/$', 'landingpage.views.account', name='account'),
    url(r'^account/logout/$', 'landingpage.views.logouting', name='logouting'),
    url(r'^account/modify/$', 'landingpage.views.modify', name='modify'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
