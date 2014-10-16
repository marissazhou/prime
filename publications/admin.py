from django.contrib import admin

from publications.models import *

class PublicationAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'author', 'abstract', 'publisher', 'publish_date')

admin.site.register(Publication, PublicationAdmin)
