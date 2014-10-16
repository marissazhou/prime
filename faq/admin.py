from django.contrib import admin

from faq.models import *

class FAQAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'body', 'created_at', 'updated_at')

admin.site.register(FAQ, FAQAdmin)
