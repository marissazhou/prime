from django.http import HttpResponse
from django.views.generic.base import View
from django.template import loader, Context
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson as json
from django.core.context_processors import csrf
import urllib2
#import pdb; pdb.set_trace()

from primemodel.models import *
from primemodel.prime import *
from primemodel.forms import BasicForm
from primemodel.logic import * 
from primemodel.utils import * 
from primemodel.DBHelper import DBHelper
from primemodel.PrimeCoordinator import PrimeCoordinator
from primemodel.PrimeOutcome import PrimeOutcome 

import os
import sys
import math 
import csv

from django.conf import settings 

def getpopulations(gender='M', limit=10):
	populations 		= Population.objects.all().order_by('created_at')[:limit]
	return populations

def getvariables():
	subsets = Variable.objects.all().order_by('created_at')
	return subsets

def getsubsets():
	subsets = PopulationSubset.objects.all().order_by('created_at')
	return subsets

def index(request):

	#test on how to use PrimeCoordinator
	eController = PrimeCoordinator()
	#get baseline and initial counterfactual exposures
#	eController.get_initial_exposures()
	#new counterfactual exposures
	"""
		the following json are for only exposures test
	"""
	json_file = '/home/zhou/Downloads/jsons/only/json_1.json'

	"""
		the following json are for compound exposures test
	"""
	#json_file = '/home/zhou/Downloads/jsons/compound/json_9.json'

	exposure_sequence = read_json(json_file)#list of exposures{mean,sd,non_rate}
 
	eController.get_counterfactual_compound_exposures(exposure_sequence)
	b_output_mortality 	= eController.output_baseline_mortality
	b_output_mortality_num 	= eController.output_baseline_mortality_num
	b_total_mortality 	= eController.output_baseline_mortality_total
	c_output_mortality 	= eController.output_counterfactual_mortality
	c_output_mortality_num 	= eController.output_counterfactual_mortality_num
	c_total_mortality 	= eController.output_counterfactual_mortality_total

	#transmit the parameters
	template = loader.get_template('primetest/index.html')
	para_view = {
			'b_output_mortality_num':	b_output_mortality_num,
			'b_total_mortality':		b_total_mortality,
			'c_output_mortality_num':	c_output_mortality_num,
			'c_total_mortality':		c_total_mortality
			}

	#context to transmit the parameters to show
	context = Context(para_view)
	response = template.render(context)
	return HttpResponse(response)


def index_test(request):
 	"""This function runs all tests with data from Anja's test excel and output the test results into file test_results_with_anja_test_excel_data.py

        :param request: request 
        :tyep request: request 
        :returns: no return 
        """
	# store test results into test_results_with_anja_test_excel_data.py
	fileaddr 	= 'primetest/test_results_with_anja_test_excel_data.py'
	f_test_result 	= open(fileaddr, 'w')
    	col1_name = 'Test Id'
    	col2_name = 'Python death total'
    	col3_name = 'Init death averted'
    	col4_name = 'Python death averted'
    	col5_name = 'Distance'
    	col6_name = 'Passed'
  	f_test_result_csv= csv.writer(open('primetest/test_results_with_anja_test_excel_data.csv', 'wb'))
	f_test_result_csv.writerow([col1_name,col2_name,col3_name,col4_name,col5_name,col6_name])
	#test on how to use ExposureController
	eController 	= PrimeCoordinator()
	"""
		the following json are for only exposures test
	"""
	exposure_sequences = read_test_parameters() # each parameter sets are in the format of exposure_sequence 
	init_results      = DBHelper.test_results # initial results in Anja's test excel
	test_results      = [] # results we get from this excel
	test_number_total = len(init_results) 
	test_number_true  = 0 
	test_percent_true = 0 
	passed = 'False' 
  	f_test_result_csv_content = [] 

	for i in range(test_number_total):
		eController.get_counterfactual_compound_exposures(exposure_sequences[i])
		c_total_mortality 	= eController.output_counterfactual_mortality_total
		c_averted_mortality 	= eController.output_total_death_averted
		distance 		= math.fabs(c_averted_mortality - float(init_results[i])) # distance between our python model result and excel test model result
		reasonable_distance 	= 0.00001 

		if distance < reasonable_distance:
			passed = 'True' 
			test_number_true = test_number_true + 1 
		else:	
			passed = 'False' 

		f_test_result.write('test			:' + str(i)+'\n')	
		f_test_result.write('python death total 	:' + str(c_total_mortality)+'\n')
		f_test_result.write('init death averted	:' + str(init_results[i])+'\n')
		f_test_result.write('python death averted 	:' + str(c_averted_mortality)+'\n')
		f_test_result.write('distance			:' + str(distance)+'\n')
		f_test_result.write('passed:' + str(passed)+'\n')
		f_test_result.flush()
		'''
			write into excel
		'''
      		#row = str(init_results[i])+ ',' + str(c_total_mortality)+ ',' + str(c_averted_mortality)+ ',' + str(distance) + ',' + str(passed)
  		#f_test_result_csv_content.append(row) 
		f_test_result_csv.writerow([str(i),str(init_results[i]),str(c_total_mortality),str(c_averted_mortality),str(distance),str(passed)])

		#print 'test			:' + str(i)
		#print 'init death averted	:' + str(init_results[i])
		#print 'python death total 	:' + str(c_total_mortality)
		#print 'python death averted 	:' + str(c_averted_mortality)
		#print 'test_number_true	:' + str(test_number_true)

	test_percent_true = test_number_true / (test_number_total+0.0) 
	f_test_result.write('test_number_true:' + str(test_number_true)+'\n')
	f_test_result.write('test_number_total:' + str(test_number_total)+'\n')
	f_test_result.write('test_percent_true :' + str(test_percent_true)+'\n')
	f_test_result.close()

	f_test_result_csv.writerow(['','','','test number true','test number total','test percent true'])
	f_test_result_csv.writerow(['','','',str(test_number_true),str(test_number_total),str(test_percent_true)])

	# write test results into csv file
	#with open('test_results_with_anja_test_excel_data.csv', 'wb') as f:
    	#	writer = csv.writer(f)
    	#	writer.writerows(f_test_result_csv_content)

	#transmit the parameters
	template = loader.get_template('primetest/index_test.html')
	para_view = {
			'init_results':			init_results,
			'test_results':			test_results,
			'test_number_total':		test_number_total,
			'test_number_true':		test_number_true,
			'test_percent_true':		test_percent_true
			}

	#context to transmit the parameters to show
	context = Context(para_view)
	response = template.render(context)
	return HttpResponse(response)

def read_test_parameters():
 	"""This function runs all tests with data from Anja's test excel and show the test results into the interface 

        :param request: request 
        :tyep request: request 
        :returns: no return 
        """
	DBHelper.get_test_data_bunch() # return DBHelper.test_exposure_sequences 
	return DBHelper.test_exposure_sequences 
