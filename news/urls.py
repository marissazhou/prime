from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('news.views',
    url(r'^$', 'index'),
    url(r'^newsdetail$', 'newsdetail'),
    (r'^articles/(\d{4})/$', 'year_archive'),
    (r'^articles/(\d{4})/(\d{2})/$', 'month_archive'),
    (r'^articles/(\d{4})/(\d{2})/(\d+)/$', 'article_detail'),
)
