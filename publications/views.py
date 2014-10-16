from django.http import HttpResponse
from django.template import loader, Context
from django.utils import simplejson

from publications.models import Publication 
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import django.utils.simplejson as json

def getarticles(limit=10):
	articles = Article.objects.all().order_by('created_at')[:limit]
	return articles


def index(request):
    a_list = Publication.objects.all()
    return render_to_response('publications/index.html', {'publication_list': a_list})


def publication_detail(request, year, month, a_id):
    a_list = Publication.objects.filter(created_at__year=year)
    article = a_list[int(a_id)]
    return render_to_response('publications/publication_detail.html', {'year': year, 'article': article})

def redirect_to_article_detail(request):
    # ...
    year = 2013
    # ...
    return HttpResponseRedirect(reverse('article_detail', args=(year, month, a_id)))
