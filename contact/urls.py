from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('contact.views',
    url(r'^$', 'index'),
    url(r'^map$', 'map'),
)
