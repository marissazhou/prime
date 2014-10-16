from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
	title 		= models.CharField(max_length=255, unique=True)
	body 		= models.TextField()
	owner		= models.ForeignKey(User, default=1)
	created_at	= models.DateTimeField(auto_now_add=True)
	updated_at	= models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['pk']
