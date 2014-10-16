"""Prime Coordination class
.. module:: PrimeCoordinator 
   :platform: Ubuntu Unix
   :synopsis: A module for common non-logic methods library 

.. moduleauthor:: Lijuan Marissa Zhou <marissa.zhou.cn@gmail.com>

"""
#from django.utils import simplejson as json
import json
import locale
from django.core.files import File

def read_json(fileaddress):
       	"""read json from fileaddress and store the content into exposures global variables, the json file format should look like [{u'non_rate': 25, u'e_id': 1, u'sd': 25, u'mean': 15.6}, {u'non_rate': 100, u'e_id': 2, u'sd': 25, u'mean': 3.6}]	

	:param fileaddress: A string to be converted
    	:type fileaddress: string 
	:returns: json content 
	"""
	json_data=open(fileaddress,'r')
	exposures = json.load(json_data)
	return exposures

def read_json_url(url): 
	"""read json from a url, the json file format should look like [{u'non_rate': 25, u'e_id': 1, u'sd': 25, u'mean': 15.6}, {u'non_rate': 100, u'e_id': 2, u'sd': 25, u'mean': 3.6}]	

	:param url: url address of json file 
    	:type url: string 
	:returns: json content 
	"""
    	f = urllib2.urlopen(url)
    	content = f.read()
    	json = simplejson.loads(content)
    	return json

def number_to_string_comma(number):
	return locale.format("%d", number, grouping=True)
