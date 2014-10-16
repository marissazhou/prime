from PrimeCoordinatorRaw import *
from DBHelperRaw import *

import os
import sys
import math 
import csv
import datetime 

def start_prime_test():
 	"""This function runs all tests with data from Anja's test excel and output the test results into file test_results_with_anja_test_excel_data.py

        :param request: request 
        :tyep request: request 
        :returns: no return 
        """
	# store test results into test_results_with_anja_test_excel_data.py
	fileaddr 	= 'test_results_with_anja_test_excel_data_command_line.txt'
	f_test_result 	= open(fileaddr, 'w')
    	col1_name = 'Test Id'
    	col2_name = 'Python death total'
    	col3_name = 'Init death averted'
    	col4_name = 'Python death averted'
    	col5_name = 'Distance'
    	col6_name = 'Passed'
  	f_test_result_csv= csv.writer(open('test_results_with_anja_test_excel_data_command_line.csv', 'wb'))
	f_test_result_csv.writerow([col1_name,col2_name,col3_name,col4_name,col5_name,col6_name])
	#test on how to use ExposureController
	eController 	= PrimeCoordinatorRaw()
	"""
		the following json are for only exposures test
	"""
	exposure_sequences 	= read_test_parameters() # each parameter sets are in the format of exposure_sequence 
	init_results      	= DBHelperRaw.test_results # initial results in Anja's test excel
	test_results      	= [] # results we get from this excel
	test_number_total 	= len(init_results) 
	test_number_true  	= 0 
	test_percent_true 	= 0 
	passed 		  	= 'False' 
  	f_test_result_csv_content = [] 

	start = datetime.datetime.now()
	print start 
	print test_number_total
	for i in range(test_number_total):
		test_start= datetime.datetime.now()
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
		f_test_result_csv.writerow([str(i),str(init_results[i]),str(c_total_mortality),str(c_averted_mortality),str(distance),str(passed)])

		print 'test			:' + str(i)
		test_end= datetime.datetime.now()
		print 'time_consumed:' + str(test_end-test_start) 

	test_percent_true = test_number_true / (test_number_total+0.0) 
	f_test_result.write('test_number_true:' + str(test_number_true)+'\n')
	f_test_result.write('test_number_total:' + str(test_number_total)+'\n')
	f_test_result.write('test_percent_true :' + str(test_percent_true)+'\n')
	f_test_result.close()

	f_test_result_csv.writerow(['','','','test number true','test number total','test percent true'])
	f_test_result_csv.writerow(['','','',str(test_number_true),str(test_number_total),str(test_percent_true)])

	end = datetime.datetime.now()
	print 'Time:'
	print end-start 

def read_test_parameters():
        """This function runs all tests with data from Anja's test excel and show the test results into the interface 

        :param request: request 
        :tyep request: request 
        :returns: no return 
        """
        DBHelperRaw.get_test_data_bunch() # return DBHelper.test_exposure_sequences 
        return DBHelperRaw.test_exposure_sequences

if __name__ == '__main__':
        """This function starts an procedure to calculate compound exposures through command line 
                the command should be in the form of:
                python PrimeCommand.py /home/zhou/Downloads/jsons/compound/json_9.json primecommandResult.csv

        :param:
        :returns: 
        """
        start_prime_test()

