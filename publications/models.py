from django.db import models
from django.contrib.auth.models import User

class Publication(models.Model):
	title 		= models.CharField(max_length=255, unique=True)
	author 		= models.ForeignKey(User, default=1)
	abstract	= models.TextField()
	publisher	= models.TextField()
	publish_date	= models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['pk']
