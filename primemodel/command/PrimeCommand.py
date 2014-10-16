"""An python command line manipulation file. This file allows user to call the python module through command line 'python PrimeCommand.py /home/zhou/Downloads/jsons/compound/json_9.json primecommandResult.csv' and calculation result will be output and stored in an excel file 
.. module:: PrimeCommand
   :platform: Ubuntu Unix, SciPy, Numpy, Mysql-Python
   :synopsis: This file composes manipulation and output through command line and output result into an excel file. 

.. moduleauthor:: Lijuan Marissa Zhou <marissa.zhou.cn@gmail.com>

"""
import sys
import utils
import logic 
import csv 
from PrimeCoordinatorRaw import *

def start_prime_coordinator():
	"""This function initializes an PrimeCoordinator object  

        :param:
        :returns: 
        """
	if len(sys.argv)<3:
    		print "\n Invalid input, please enter correct parameters \n use command like: \n\t python PrimeCommand.py parameters_json.json primecommandResult.csv\n"
    		sys.exit(0)

  	#store command line arguments to local variables
  	json_file = sys.argv[1]
  	result_file = sys.argv[2]
	exposure_sequence = utils.read_json(json_file)#list of exposures{mean,sd,non_rate}, read json content into memory

        primeCoordinator = PrimeCoordinatorRaw()
        primeCoordinator.get_counterfactual_compound_exposures(exposure_sequence)

 	# get the data to print/store in a file 
        b_output_mortality      = primeCoordinator.output_baseline_mortality
        b_output_mortality_num  = primeCoordinator.output_baseline_mortality_num
        b_total_mortality       = primeCoordinator.output_baseline_mortality_total
        c_output_mortality      = primeCoordinator.output_counterfactual_mortality
        c_output_mortality_num  = primeCoordinator.output_counterfactual_mortality_num
        c_total_mortality       = primeCoordinator.output_counterfactual_mortality_total
        total_population        = primeCoordinator.output_total_population
        #total_death_averted    = str(int(round(primeCoordinator.output_total_death_averted))) # int
        total_death_averted     = str(primeCoordinator.output_total_death_averted) # decimale
        total_death_baseline    = str(primeCoordinator.output_total_death_baseline)

        '''
                These are the outputs 
        '''
        all_mortality_outcome	= primeCoordinator.output_all_mortality_exposure_outcome # [{'outcome_id':outcome_id,'name':outcome name,'baseline_death':100, 'counterfactual_death':20},{}] 
        all_mortality_age       = primeCoordinator.output_all_mortality_age # [{'age_group_id':age_group_id,'age_group':age_group,'baseline_death':100, 'counterfactual_death':20},{}] 
        all_mortality_gender    = primeCoordinator.output_all_mortality_gender# [{'gender':'male','baseline_death':100, 'counterfactual_death':20},{'gender':'female','baseline_death':100, 'counterfactual_death':20}] 

        '''
                Write results into a csv file
        '''
        f_test_result_csv= csv.writer(open(result_file, 'wb')) # write result into csv
	# write over all attributions 
	col1_name = 'total population'
        f_test_result_csv.writerow([col1_name]) # write title
       	f_test_result_csv.writerow([total_population]) # write baseline and counterfactual mortalities 
        f_test_result_csv.writerow([]) # write seperate line 
	col1_name = 'total death averted'
        f_test_result_csv.writerow([col1_name]) # write title
       	f_test_result_csv.writerow([total_death_averted]) # write baseline and counterfactual mortalities 
        f_test_result_csv.writerow([]) # write seperate line 
		
	# write all mortality by outcome 
	col1_name = 'outcome_id'
	col2_name = 'name'
        col3_name = 'b_mortality_sum_db'
        col4_name = 'c_mortality_sum'
        f_test_result_csv.writerow([col1_name,col2_name,col3_name,col4_name]) # write title
	for line in all_mortality_outcome:
        	f_test_result_csv.writerow([line.get(col1_name),line.get(col2_name),line.get(col3_name),line.get(col4_name)]) # write baseline and counterfactual mortalities 
        f_test_result_csv.writerow([]) # write seperate line 
		
	# write all mortality by age 
	col1_name = 'age_group_id'
	col2_name = 'age_group'
        col3_name = 'b_mortality_sum_db'
        col4_name = 'c_mortality_sum'
        f_test_result_csv.writerow([col1_name,col2_name,col3_name,col4_name]) # write title
	for line in all_mortality_age:
        	f_test_result_csv.writerow([line.get(col1_name),line.get(col2_name),line.get(col3_name),line.get(col4_name)]) # write baseline and counterfactual mortalities 
        f_test_result_csv.writerow([]) # write seperate line 
		
	# write all mortality by gender
	col1_name = 'gender'
        col2_name = 'b_mortality_sum_db'
        col3_name = 'c_mortality_sum'
        f_test_result_csv.writerow([col1_name,col2_name,col3_name]) # write title
	for line in all_mortality_gender:
        	f_test_result_csv.writerow([line.get(col1_name),line.get(col2_name),line.get(col3_name)]) # write baseline and counterfactual mortalities 
        f_test_result_csv.writerow([]) # write seperate line 
		

    
if __name__ == '__main__': 
	"""This function starts an procedure to calculate compound exposures through command line 
		the command should be in the form of:
		python PrimeCommand.py /home/zhou/Downloads/jsons/compound/json_9.json primecommandResult.csv

        :param:
        :returns: 
        """
	start_prime_coordinator() 
