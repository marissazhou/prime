from django import forms

# from primemodel.models import *

class BasicForm(forms.Form):
	mean	= forms.CharField(max_length=255) 
	sd 		= forms.CharField(max_length=255)