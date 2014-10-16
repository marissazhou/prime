"""An Exposure Class
.. module:: PrimeExposure 
   :platform: Ubuntu Unix
   :synopsis: A module for concluding all exposure relavant data and operation.

.. moduleauthor:: Lijuan Marissa Zhou <marissa.zhou.cn@gmail.com>

"""
import copy
from primemodel.models import *
from primemodel.prime import *
from primemodel.DBHelper import DBHelper 

class PrimeExposure():

	def __init__(self, exposure_id, outcome_ids, compound_outcome_ids, mortalities, bins_rr, bins_pop, outcomes, popDistribution):
		""" initialization by assigning attributes and calculating exposure distribution and outcome data

    		:param e_id: exposure id.
    		:type e_id: int
    		:param outcome_ids: related outcome ids.
    		:type outcome_ids: list 
    		:param compound_outcome_ids: all related outcome ids including relevant outcome ids from previous exposures, this is for representing in the interface.
    		:type compound_outcome_ids: Set 
    		:param mortalities: original mortalities for calculating couterfactual mortalities. Values stored in a list
    		:type mortalities: list 
    		:param bins_rr: bins used for outcome relative risks calculation, bins are kept same for all outcomes within one exposure 
    		:type bins_rr: list 
    		:param bins_pop: bins used for population distribution calculation
    		:type bins_pop: list 
    		:param outcomes: list of PrimeOutcome objects, each object stores information of one outcome within exposure  
    		:type outcomes: list 
    		:param popDistribution: An object of ExposureDistribution, this object stores information of the population information for both baseline and counterfactual population distributions 
    		:type popDistribution: ExposureDistribution 
   	 	:returns: 
		:raises: AttributeError, KeyError
    		"""
		self.exposure_id 	= exposure_id # exposure id, same as in the database table primemodel_exposure 
		self.outcome_ids	= outcome_ids # outcome ids for all affected outcomes in a compound exposure list. [{o_id:o_id,lle:lle,ule:ule,measure:measure}]
		self.compound_outcome_ids= compound_outcome_ids # [o_id_1, o_id_2...]
		self.mortalities	= mortalities # original mortality
		self.bins_rr 		= bins_rr # bins for relative risk
		self.bins_pop 		= bins_pop # bins for population distribution
		self.outcomes 		= outcomes # all associated outcomes of current expsoure, {id:Outcome}
		self.popDistribution 	= popDistribution # the population distribution of current exposure, it includes baseline and counterfactual distribution. Baseline distribution is necessary for calcuation death rates, counterfactual distribution is necessary for calculating counterfactual deaths and final death averted.
		
		'''
			starts to calculate the data for population and outcome. This process does not start until and exposure instance is initiated.
		'''
		self.get_population_distributions() # starts to calculate all population subsets distribution over different bins
		self.get_outcomes_distributions() # starts to fulfill outcome by calculating relative risks, deaths rates and deaths.

	#################################################
	# distribution					#
	#################################################
	def get_population_distributions(self):
		"""This function starts to generate population distribution for current exposure, all population subsets distribution. 

    		:param self: self attributes 
   	 	:returns: No return 
    		"""
		self.popDistribution.get_population_distributions(self.exposure_id) # call the population distribution calculation function in PopDistribution to get the population

	#################################################
	# outcome					#
	#################################################
	def get_outcomes_distributions(self):
		""" starts to generate outcome distribution, including relative risk, death rates and deaths. 

    		:param self: self attributes 
   	 	:returns: No return 
    		"""
		# baseline population distribution
		b_dist = self.popDistribution.get_attr_b_distribution()
		# counterfactual population distribution
		c_dist = self.popDistribution.get_attr_c_distribution()
		# related outcome keys 
		keys   = self.outcomes.keys()
		# fulfill all outcomes' data: relative risk, death rate and deaths
		for key in keys: # keys are outcome id list
			outcome = self.outcomes[key] #outcome is a PrimeOutcome class object/instance, self.outcomes are all assigned outcomes dictionary, in a form of {outcome_id:PrimeOutcome instance,...} 
			outcome.get_relative_risk() # calculating relative risks
			outcome.get_death_rates(b_dist)	# when calculation death rates, the first element relies on the baseline population distribution	
			outcome.get_deaths(b_dist,c_dist) # calculating both baseline deaths and counterfactual deaths. Baseline deaths can be avoided if more efficiency is needed. 
			outcome.get_c_mortality() # counterfactual mortality
		# fulfill counterfactual mortalities list for current exposure
		self.get_c_mortalities() # counterfactual mortalities for all outcomes in the current exposure

	def get_outcomes_relative_risks(self):
		""" return a list of relative risks for all outcomes of this exposure 

    		:param self: self attributes 
   	 	:returns: No return 
    		"""
		relative_risks = {}
		# calculate relative risks for all outcomes
		for outcome in self.outcomes:
			o_id 			= outcome.get_attr_id() # outcome id
			relative_risks[o_id]	= outcome.get_attr_m_relative_risks() # relative risk
		return relative_risks

	def get_outcome(self, outcome_id):
		""" return outcome at outcome_id, not necessary for current ages 

    		:param outcome_id: id of outcome 
    		:type outcome_id: int 
   	 	:returns: an Outcome object 
    		"""
		return self.outcomes[outcome_id]

	def get_outcome_deaths_sum(self, i, is_baseline):
		""" return deaths sum for baseline or counterfactual 

    		:param is_baseline: true is baseline, false is counterfactual 
    		:type is_baseline: bool 
   	 	:returns: death sum  
    		"""
		outcome 	= self.outcomes[i]	
		deaths_sum 	= 0 
		deaths_sum 	= outcome.get_deaths_sum(is_baseline)  
		return deaths_sum

	def get_age_deaths_sum(self, a_id):
		""" return deaths sum for a specific age group 

    		:param a_id: age group id 
    		:type a_id: int 
   	 	:returns: death sum  
    		"""
		deaths_sum 	= 0 
		for o_id in self.outcomes:
			outcome	    = self.outcomes[o_id]	
			deaths_sum += outcome.get_deaths_sum(True)  
			deaths_sum += outcome.get_deaths_sum(False)  
		return deaths_sum

	def get_outcome_death_rates(self, o_id):
		""" return deaths rates for ith outcome 

    		:param o_id: outcome id
    		:type o_id: int 
   	 	:returns: death sum  
    		"""
		outcome 	= self.outcomes[o_id]	
		death_rates 	= outcome.get_attr_death_rates()
		return death_rates

	def get_outcome_mortality(self, o_id, is_baseline):
		""" return deaths sum for outcome o_id, baseline or counterfactual 

    		:param is_baseline: true is baseline, false is counterfactual 
    		:type is_baseline: bool 
   	 	:returns: death sum for outcome o_id 
    		"""
		outcome 	= self.outcomes[o_id]	
		mortalities 	= None
		if is_baseline: #baseline
			mortalities 	= outcome.get_attr_b_mortality()
		else: #counterfactual
			mortalities 	= outcome.get_attr_c_mortality()
		return mortalities # [mortality for each age group] 

	def get_c_mortalities(self):
		""" return final counterfactual mortality, same format as DBHelper.mortalities, aka the origianl mortality 

    		:param self: self attributes 
   	 	:returns: No return 
    		"""
		self.c_mortalities 		= copy.deepcopy(self.mortalities) # copy original mortalities, can not be '=' and it will be just a reference 
		self.c_mortalities_outcome 	= {} # {o_id: mortality number} 
		keys 				= self.outcome_ids.keys() # outcome_ids = {id:{lle,ule,measure}}
		for o_id in keys: # keys are all outcome ids
			mortality 		= self.get_outcome_mortality(o_id,False)
			self.c_mortalities[o_id]= mortality # {o_id: [mortality number]} 
		keys = self.c_mortalities.keys() # keys for all outcomes 
		for o_id in keys:
			self.c_mortalities_outcome[o_id]= sum(self.c_mortalities.get(o_id)) #{o_id: mortality number} 

		# get more mortalities to represent
		self.get_c_mortalities_age_and_gender()

	def get_c_mortalities_age_and_gender(self):
		age_sep 				= DBHelper.age_group_num/2 + 1
		self.c_mortalities_age			= {} # {age_group_id: mortality number} 
		for age_id in range(1, DBHelper.age_group_num + 1): # initiate mortality in all age groups to be 0
			self.c_mortalities_age[age_id] 	= 0 # {age_group_id: mortality number} 
		self.c_mortalities_gender		= {} # {'male': 0, 'female':1} 
		sum_mortality_male 			= 0 # 
		sum_mortality_female 			= 0 # 
		
		keys 					= self.c_mortalities.keys() # keys for all outcomes 
		for o_id in keys:
			outcome_mortality = self.c_mortalities[o_id] # [mortality for each age group]
			for age_id in range(1, DBHelper.age_group_num + 1): # 
				mortality_current_age_group 	= self.c_mortalities_age[age_id] #
				self.c_mortalities_age[age_id] 	= mortality_current_age_group + outcome_mortality[age_id - 1] # {age_group_id: mortality number} 
				if age_id < age_sep:
					sum_mortality_male = sum_mortality_male + outcome_mortality[age_id] # {age_group_id: mortality number}    
				else:
					sum_mortality_female = sum_mortality_female + outcome_mortality[age_id -1] # {age_group_id: mortality number}    
		self.c_mortalities_gender['male']	= sum_mortality_male # 
		self.c_mortalities_gender['female']	= sum_mortality_female # 
		
			
	#################################################
	# get and set attributions			#
	#################################################
	def get_attr_bins_rr(self):
		""" return class attribution samples/bins for outcome 

    		:param self: self attributes 
   	 	:returns: samples for outcome 
    		"""
		return self.bins_rr
		
	def get_attr_bins_pop(self):
		""" return class attribution samples/bins for population 

    		:param self: self attributes 
   	 	:returns: samples for population 
    		"""
		return self.bins_pop

	def get_attr_population_distribution(self):
		""" return class attribution population distribution 

    		:param self: self attributes 
   	 	:returns: population distribution 
    		"""
		return self.popDistribution
		
	def get_attr_mortality_counterfactual(self):
		""" return class attribution population distribution 

    		:param self: self attributes 
   	 	:returns: population distribution 
    		"""
		return self.c_mortalities

	def set_attr_mortalities(self, mortalities):
		""" return class attribution mortalities 

    		:param self: self attributes 
   	 	:returns: original mortalities  
    		"""
		self.mortalities = mortalities
		
