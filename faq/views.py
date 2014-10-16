from django.http import HttpResponse
from django.template import loader, Context
from django.utils import simplejson

from faq.models import FAQ 
import django.utils.simplejson as json
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def index(request):
    faq_list = FAQ.objects.all()
    return render_to_response('faq/index.html', {'faq_list': faq_list})

def redirect_to_article_detail(request):
    # ...
    year = 2013
    month = 5 
    a_id = 1 
    # ...
    return HttpResponseRedirect(reverse('faq_list', args=(year, month, a_id)))
