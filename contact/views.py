from django.http import HttpResponse
from django.template import loader, Context

def index(request):
	template = loader.get_template('contact/index.html')
	context = Context({})
	response = template.render(context)
	return HttpResponse(response)

def map(request):
	template = loader.get_template('contact/map.html')
	context = Context({})
	response = template.render(context)
	return HttpResponse(response)

