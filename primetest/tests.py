"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from primemodel.PrimeCoordinator import PrimeCoordinator
from primemodel.logic import * 


class SimpleTest(TestCase):
    def test_get_balanced_cholestrol_fat(self):
    	"""
    	Test for fruit exposure example by marissa 
    	"""
	# Test for Fruit
    	actual_mean			= 1.55# This data to be extracted from a database table with values provided by Anja
	fat_means			= [37.3, 14.1, 13.7, 6.8, 250]
	mean 				= get_balanced_mean(fat_means)
	# calculation result
    	self.assertEqual(actual_mean, mean)

    def test_bmi_counterfactual_mean(self):
    	"""
    	Test for fruit exposure example by marissa 
    	"""
	#test on how to use PrimeCoordinator 
	primeCoordinator 		= PrimeCoordinator()

	# Test for Fruit
    	actual_deaths_averted 	  	= 256420 # This data to be extracted from a database table with values provided by Anja
	exposure_sequence 		= [{u'non_rate': 0, u'e_id': 1, u'sd': 37.72, u'mean': 200.0}]
	primeCoordinator.get_counterfactual_compound_exposures(exposure_sequence)
	# calculation result
	calculated_deaths_averted	= round(primeCoordinator.output_counterfactual_mortality_total)
    	self.assertEqual(calculated_deaths_averted, actual_deaths_averted)

    def test_veg(self):
    	"""
    	Test for veg exposure example by marissa 
    	"""
	#test on how to use PrimeCoordinator 
	primeCoordinator 			= PrimeCoordinator()

	# Test for Veg 
    	actual_deaths_averted 	  	= 256420 # This data to be extracted from a database table with values provided by Anja
	exposure_sequence 		= [{u'non_rate': 0, u'e_id': 2, u'sd': 33.6, u'mean': 180.0}]
	primeCoordinator.get_counterfactual_compound_exposures(exposure_sequence)
	# calculation result
	calculated_deaths_averted	= round(primeCoordinator.output_counterfactual_mortality_total)
    	self.assertEqual(calculated_deaths_averted, actual_deaths_averted)

    def test_fibre(self):
    	"""
    	Test for fibre exposure example by marissa 
    	"""
	#test on how to use PrimeCoordinator 
	primeCoordinator 			= PrimeCoordinator()

	# Test for Fibre 
    	actual_deaths_averted 	  	= 253405 	# This data to be extracted from a database table with values provided by Anja
	exposure_sequence 		= [{u'non_rate': 0, u'e_id': 3, u'sd': 1.55, u'mean': 18}]
	primeCoordinator.get_counterfactual_compound_exposures(exposure_sequence)
	# calculation result
	calculated_deaths_averted	= round(primeCoordinator.output_counterfactual_mortality_total)
    	self.assertEqual(calculated_deaths_averted, actual_deaths_averted)

    def test_salt(self):
    	"""
    	Test for salt exposure example by marissa 
    	"""
	#test on how to use PrimeCoordinator 
	primeCoordinator 			= PrimeCoordinator()

	# Test for Salt 
    	actual_deaths_averted 	  	= 248226 # This data to be extracted from a database table with values provided by Anja
	exposure_sequence 		= [{u'non_rate': 0, u'e_id': 4, u'sd': 0.9, u'mean': 6}]
	primeCoordinator.get_counterfactual_compound_exposures(exposure_sequence)
	# calculation result
	calculated_deaths_averted	= round(primeCoordinator.output_counterfactual_mortality_total)
    	self.assertEqual(calculated_deaths_averted, actual_deaths_averted)

    def test_fat(self):
    	"""
    	Test for fat exposure example by marissa 
    	"""
	#test on how to use PrimeCoordinator 
	primeCoordinator 			= PrimeCoordinator()

	# Test for Fat 
    	actual_deaths_averted 	  	= 254938 # This data to be extracted from a database table with values provided by Anja
	exposure_sequence 		= [{u'non_rate': 0, u'e_id': 5, u'sd_total': 0.9, u'mean_total': 5, u'sd_sat': 0.9, u'mean_sat': 5, u'sd_mufa': 0.9, u'mean_mufa': 5, u'sd_pufa': 0.9, u'mean_pufa': 5, u'sd_diet': 0.9, u'mean_diet': 5}]
	primeCoordinator.get_counterfactual_compound_exposures(exposure_sequence)
	# calculation result
	calculated_deaths_averted	= round(primeCoordinator.output_counterfactual_mortality_total)
    	self.assertEqual(calculated_deaths_averted, actual_deaths_averted)

    def test_pa(self):
    	"""
    	Test for physical activity exposure example by marissa 
    	"""
	#test on how to use PrimeCoordinator 
	primeCoordinator 			= PrimeCoordinator()

	# Test for PA 
    	actual_deaths_averted 	  	= 256616# This data to be extracted from a database table with values provided by Anja
	exposure_sequence 		= [{u'non_rate': 0, u'e_id': 6, u'sd': 35, u'mean': 35}]
	primeCoordinator.get_counterfactual_compound_exposures(exposure_sequence)
	# calculation result
	calculated_deaths_averted	= round(primeCoordinator.output_counterfactual_mortality_total)
    	self.assertEqual(calculated_deaths_averted, actual_deaths_averted)

    def test_bmi(self):
    	"""
    	Test for bmi exposure example by marissa 
    	"""
	#test on how to use PrimeCoordinator 
	primeCoordinator 			= PrimeCoordinator()

	# Test for BMI 
    	actual_deaths_averted 	  	= 263185# This data to be extracted from a database table with values provided by Anja
	exposure_sequence 		= [{u'non_rate': 0, u'e_id': 7, u'sd': 35, u'mean': 35}]
	primeCoordinator.get_counterfactual_compound_exposures(exposure_sequence)
	# calculation result
	calculated_deaths_averted	= round(primeCoordinator.output_counterfactual_mortality_total)
    	self.assertEqual(calculated_deaths_averted, actual_deaths_averted)

    def test_alcohol(self):
    	"""
    	Test for alcohol exposure example by marissa 
    	"""
	#test on how to use PrimeCoordinator 
	primeCoordinator 			= PrimeCoordinator()

	# Test for Alcohol 
    	actual_deaths_averted 	  	= 260100# This data to be extracted from a database table with values provided by Anja
	exposure_sequence 		= [{u'non_rate': 20, u'e_id': 8, u'sd': 10, u'mean': 8}]
	primeCoordinator.get_counterfactual_compound_exposures(exposure_sequence)
	# calculation result
	calculated_deaths_averted	= round(primeCoordinator.output_counterfactual_mortality_total)
    	self.assertEqual(calculated_deaths_averted, actual_deaths_averted)

    def test_smoking(self):
    	"""
    	Test for smoking exposure example by marissa 
    	"""
	#test on how to use PrimeCoordinator 
	primeCoordinator 			= PrimeCoordinator()

	# Test for Smoking 
    	actual_deaths_averted 	  	= 248037# This data to be extracted from a database table with values provided by Anja
	exposure_sequence 		= [{u'non_rate': 0.5, u'e_id': 9, u'sd': 0.2, u'mean': 0.3}]
	primeCoordinator.get_counterfactual_compound_exposures(exposure_sequence)
	# calculation result
	calculated_deaths_averted	= round(primeCoordinator.output_counterfactual_mortality_total)
    	self.assertEqual(calculated_deaths_averted, actual_deaths_averted)
