from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('publications.views',
    url(r'^$', 'index'),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)
