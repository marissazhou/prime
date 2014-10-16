from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('primetest.views',
    url(r'^$', 'index'),
    url(r'^index_test$', 'index_test'),
)
