"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from primemodel.PrimeCoordinator import PrimeCoordinator
from primemodel.logic import * 


class SimpleTest(TestCase):
    def test_bmi_counterfactual_mean(self):
    	actual_bmi_c_mean 		= 21.128010725 # This data to be extracted from a database table with values provided by Anja
	#bmi_mean_c = get_bmi_counterfactual_mean(b_bmi_mean, b_energy_mean, c_energy_mean, b_height_mean, b_sedentary_rate, b_met_mean, b_met_mvpa, b_met_non_mvpa, c_sedentary_rate, c_met_mean, c_met_mvpa, c_met_non_mvpa)
	b_bmi_mean = 20
	b_energy_mean = 2000 
	c_energy_mean = 2100
	b_height_mean = 1.776
	b_sedentary_rate = 0
	b_met_mean = 30
	b_met_mvpa = 6.0
	b_met_non_mvpa = 1.1 
	c_sedentary_rate = 0
	c_met_mean = 35
	c_met_mvpa = 6.0
	c_met_non_mvpa = 1.1 
	
	bmi_mean_c = get_bmi_counterfactual_mean(b_bmi_mean, b_energy_mean, c_energy_mean, b_height_mean, b_sedentary_rate, b_met_mean, b_met_mvpa, b_met_non_mvpa, c_sedentary_rate, c_met_mean, c_met_mvpa, c_met_non_mvpa)
    	self.assertEqual(round(bmi_mean_c,10),actual_bmi_c_mean)

    def test_pal_active(self):
    	actual_pal_active = 1.2701388889# This data to be extracted from a database table with values provided by Anja
	met_mean = 35
	met_mvpa = 6.0
	met_non_mvpa = 1.1 
	pal_active_test = get_pal_active(met_mean, met_mvpa, met_non_mvpa)
    	self.assertEqual(round(pal_active_test,10),actual_pal_active)

    def test_pal_mean(self):
	sedentary_rate = 0
	met_mean = 35
	met_mvpa = 6.0
	met_non_mvpa = 1.1 
    	actual_pal_mean= 1.2701388889# This data to be extracted from a database table with values provided by Anja
	pal_mean= get_pal_mean(sedentary_rate, met_mean, met_mvpa, met_non_mvpa)
    	self.assertEqual(round(pal_mean,10),actual_pal_mean)

    def test_fruit(self):
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
