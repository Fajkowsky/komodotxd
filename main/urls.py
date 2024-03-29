from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

handler404 = 'landingpage.views.error'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'main.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('landingpage.urls')),
    url(r'^admin/', include(admin.site.urls)),
)