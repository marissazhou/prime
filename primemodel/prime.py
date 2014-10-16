"""
	Needs cleaning up 
		- lots of test code here... 
		- need to move all this business-logic over to the primelogic/logic.py library
"""

from primemodel.models import *

from common.utils import *

def test_myprime():
	
	return [1,2,3,4]

def get_variables():
	variables = Variable.objects.all().order_by('created_at')
	return variables

def get_variable_data(variable):

	return { 'variable': variable } 

def get_population_data():

	# Define limited population for now
	population_size = PopulationSubset.objects.get(gender='M', age_group='15-19').size
	return { 'population': '15-19', 'gender': 'M', 'size': population_size }

def get_measurement_data(variable):

	# # # measurements = Measurement.objects.filter(, measurement_type__variable__name=variable, measurement_type__statistical_measure='Mean')
	# # # for measurement in measurements:
	# # # 	print m.population_subset.gender, m.population_subset.age_group, m.measurement_option, m.value

	# Define baseline and counterfactual basic distribution statistics
	measurements_data = {}
	measurements_data['baseline_mean'] 	= float(Measurement.objects.get(population_subset__gender='M', population_subset__age_group='15-19', measurement_type__variable__name=variable, measurement_type__statistical_measure='Mean', measurement_option='B').value)
	measurements_data['baseline_sd'] 	= float(Measurement.objects.get(population_subset__gender='M', population_subset__age_group='15-19', measurement_type__variable__name=variable, measurement_type__statistical_measure='SD', measurement_option='B').value)
	measurements_data['cf_mean'] 		= float(Measurement.objects.get(population_subset__gender='M', population_subset__age_group='15-19', measurement_type__variable__name=variable, measurement_type__statistical_measure='Mean', measurement_option='C').value)
	measurements_data['cf_sd'] 			= float(Measurement.objects.get(population_subset__gender='M', population_subset__age_group='15-19', measurement_type__variable__name=variable, measurement_type__statistical_measure='SD', measurement_option='C').value)
	return measurements_data

# This needs to be extracted from the database
def get_distribution_data(data):
	
	distribution_data 	= 	[
										{
										'lower': 0,
										'upper': 2,
										'range': '<2',
										'midpoint': 1
										},
										{
										'lower': 2,
										'upper': 4,
										'range': '2-4',
										'midpoint': 3
										},
										{
										'lower': 4,
										'upper': 6,
										'range': '4-6',
										'midpoint': 5
										},
										{
										'lower': 6,
										'upper': 8,
										'range': '6-8',
										'midpoint': 7
										},
										{
										'lower': 8,
										'upper': 10,
										'range': '8-10',
										'midpoint': 9
										},
										{
										'lower': 10,
										'upper': 12,
										'range': '10-12',
										'midpoint': 11
										},
										{
										'lower': 12,
										'upper': 14,
										'range': '12-14',
										'midpoint': 13
										},
										{
										'lower': 14,
										'upper': 16,
										'range': '14-16',
										'midpoint': 15
										},
										{
										'lower': 16,
										'upper': 18,
										'range': '16-18',
										'midpoint': 17
										},
										{
										'lower': 18,
										'upper': 20,
										'range': '18-20',
										'midpoint': 19
										},
										{
										'lower': 20,
										'upper': 22,
										'range': '20-22',
										'midpoint': 21
										},
										{
										'lower': 22,
										'upper': 24,
										'range': '22-24',
										'midpoint': 23
										},
										{
										'lower': 24,
										'upper': 26,
										'range': '24-26',
										'midpoint': 25
										},
										{
										'lower': 26,
										'upper': 28,
										'range': '26-28',
										'midpoint': 27
										},
										{
										'lower': 28,
										'upper': 30,
										'range': '28-30',
										'midpoint': 29
										}
										]

	ddata = []
	for bucket in distribution_data:

		lower 	 = bucket['lower']
		upper 	 = bucket['upper']
		rval 	 = bucket['range']
		midpoint = bucket['midpoint']

		bucket['baseline_dist_value'] 	= calc_baseline_dist(
															data['population_data']['measurements']['baseline_mean'], 
															data['population_data']['measurements']['baseline_sd'], 
															data['population_data']['population']['size'], 
															upper, 
															lower
															)
		bucket['cf_dist_value'] 		= calc_baseline_dist(
															data['population_data']['measurements']['cf_mean'], 
															data['population_data']['measurements']['cf_sd'], 
															data['population_data']['population']['size'], 
															upper, 
															lower
															)

		ddata.append(bucket)

	return ddata

def get_baseline_stats(variable):

	# All variables are capitalized in the database
	variable = variable.capitalize()

	#Get data
	variable_data 		= get_variable_data(variable)
	population_data 	= get_population_data()
	measurements_data 	= get_measurement_data(variable)

	population_data = { 
						'population': population_data, 
						'measurements': measurements_data,
						}
	data = { 
			'variable': variable_data, 
			'population_data': population_data,			
			}

	data['population_data']['distribution_data'] = get_distribution_data(data)



	return data

