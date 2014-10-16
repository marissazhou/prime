from django.contrib import admin

from news.models import *

class ArcticleAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'body', 'owner', 'created_at', 'updated_at')

admin.site.register(Article, ArcticleAdmin)
