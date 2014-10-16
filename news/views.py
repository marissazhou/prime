from django.http import HttpResponse
from django.template import loader, Context
from django.utils import simplejson

from news.models import Article
import django.utils.simplejson as json
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def getarticles(limit=10):
	articles = Article.objects.all().order_by('created_at')[:limit]
	return articles


def index_static(request):
	articles = getarticles()
	template = loader.get_template('news/index.html')
	context = Context({'articles': articles})
	response = template.render(context)
	return HttpResponse(response)

def index(request):
    a_list = Article.objects.all()
    return render_to_response('news/index.html', {'article_list': a_list})

def newsdetail(request):
	articles = getarticles()
	template = loader.get_template('news/newsdetail.html')
	context = Context({'articles': articles})
	response = template.render(context)
	return HttpResponse(response)

def year_archive(request, year):
    a_list = Article.objects.filter(created_at__year=year)
    return render_to_response('news/year_archive.html', {'year': year, 'article_list': a_list})

def month_archive(request, year, month):
    a_list = Article.objects.filter(created_at__year=year)
    return render_to_response('news/month_archive.html', {'year': year, 'article_list': a_list})

def article_detail(request, year, month, a_id):
    a_list = Article.objects.filter(created_at__year=year)
    article = a_list[int(a_id)]
    return render_to_response('news/article_detail.html', {'year': year, 'article': article})

def redirect_to_article_detail(request):
    # ...
    year = 2013
    month = 5 
    a_id = 1 
    # ...
    # return HttpResponseRedirect(reverse('news.views.year_archive', args=(year, month, a_id)))
    return HttpResponseRedirect(reverse('article_detail', args=(year, month, a_id)))
