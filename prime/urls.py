from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Add url file for primemodel/urls.py
    # url(r'^prime/', include('prime.urls')),
    url(r'^prime/', include('primemodel.urls')),
	# Add url file for news/urls.py
    url(r'^news/', include('news.urls')),
	# Add url file for publications/urls.py
    url(r'^publications/', include('publications.urls')),
	# Add url file for faq/urls.py
    url(r'^faq/', include('faq.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^primetest/', include('primetest.urls')),
    # url(r'^$', 'prime.views.home', name='home'),
    # url(r'^prime/', include('prime.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
