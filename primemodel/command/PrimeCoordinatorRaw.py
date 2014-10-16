"""Prime Coordination class. This is the main class that users can call and use its functions to generate either single exposure or exposure list. 
	It does three main things:
		1. initiate database, fetch all measurements, references, exposure outcome relationships, etc.
		2. generate exposures, either a single exposure or exposure lists, namely compound expsoures 
		3. manipulate exposures, including getting total final mortality, getting averted mortality etc. 
.. module:: PrimeCoordinator 
   :platform: Ubuntu Unix
   :synopsis: A module for operating all exposures compound or only, baseline or counterfactual.

.. moduleauthor:: Lijuan Marissa Zhou <marissa.zhou.cn@gmail.com>

"""
from PopDistributionRaw import * 
from PrimeExposureRaw  import * 
from PrimeOutcomeRaw  import * 
from DBHelperRaw import * 
from logic import * 
from utils import * 
from sets import Set

import unicodedata

class PrimeCoordinatorRaw():

	"""
		exposure objects, both for only ones and compound ones
	"""
	only_exposures	= {} # a dict of only exposures {exposure_id:exposure object}
	cc_exposures	= [] # new counterfactual compound exposures
	
	"""
		deaths to show in the webpages [age]
	"""
	output_total_population			= 0 #sum(DBHelperRaw.population_subsets)  
	output_total_death_baseline		= 0 # all death in baseline
	output_total_death_averted		= 0 # all death averted
	output_baseline_mortality		= {} # {o_id:[]} {outcome_id:[deaths for population subsets]}
	output_baseline_mortality_num		= [] # [death sum for outcome]
	output_baseline_mortality_total		= 0  # sum of all outcome mortalities 
	output_counterfactual_mortality		= {} # {o_id:[]} {outcome_id:[deaths for population subsets]}
	output_counterfactual_mortality_num	= [] # [death sum for outcome]
	output_counterfactual_mortality_total	= 0  # sum of all outcome mortalities 
	output_all_mortality_exposure_outcome	= []  # [{'outcome_id':outcome_id,'name':outcome name,'baseline_death':100, 'counterfactual_death':20},{}] 
	output_all_mortality_age		= []  # [{'age_group_id':age_group_id,'age_group':age_group,'baseline_death':100, 'counterfactual_death':20},{}] 
	output_all_mortality_gender		= []  # [{'gender':'male','baseline_death':100, 'counterfactual_death':20},{'gender':'female','baseline_death':100, 'counterfactual_death':20}] 


	def __init__(self):
    		"""This function initializes an PrimeCoordinator object  

    		:param:
   	 	:returns: 
    		"""
		DBHelperRaw.initialize() #initiate dababase helper
		self.output_total_population	= number_to_string_comma(DBHelperRaw.population_total_size)  # sum up of all populations
		self.refresh_output_baseline_mortality() # refresh final compound mortality

	#################################################
	# outcomes					# 
	#################################################
	def get_exposure(self, exposure_id, b_mean, b_sd, c_mean, c_sd, b_non_rate, c_non_rate, dist_type, mortalities, outcome_ids, pre_compound_outcome_ids):#id in db
    		"""This function initiates an exposure object, it also calculates all population distributions and outcome relative risks, death rates and deaths and final counterfactual mortality.  

    		:param exposure_id: id for exposures
    		:type exposure_id: int
    		:param b_mean: mean for baseline 
    		:type b_mean: array
    		:param b_sd: standard deviation for counterfactual 
    		:type b_sd: array
    		:param c_mean: mean for baseline 
    		:type c_mean: array
    		:param c_sd: standard deviation for counterfactual 
    		:type c_sd: array
    		:param non_rate: non rate for smokers/drinkers 
    		:type non_rate: array
    		:param dist_type: distribution type 0: normal distribution; 1: lognormal distribution; 2: binary distribution 
    		:type dist_type: int 
    		:param mortalities: baseline mortalities for a new exposure, could be mortality in db or counterfactual mortality of previous exposure, {outcome_id:[mortalities of current outcome]} 
    		:type mortalities: dict 
    		:param outcome_ids: all outcome attributes for affected outcomes 
    		:type outcome_ids: list 
    		:param pre_compound_outcome_ids: all affected outcome ids for compound exposures, [1,2,3....] 
    		:type pre_compound_outcome_ids: list 
   	 	:returns: an exposure object 
   	 	:raises: an exception 
    		"""
		e_id 		= int(exposure_id) # exposure id
		exposure_bins_rr= DBHelperRaw.exposure_bins_rr.get(e_id) #bins to define the relative risks of the exposure within population. (e.g. salt [1,3,5,...]) 
		exposure_bins 	= DBHelperRaw.exposure_bins.get(e_id) #bins to define the exposure within population (e.g. salt [0-2,2-4,4-6,...]), the upper limit is chosen to store as the bins 
		risks 		= DBHelperRaw.risks.get(e_id) #initial risks for all population subsets of the current exposures, including relative risks for all outcomes related to current exposure and stored in a dictionary like {outcome_id:[relative risks for all population subsets]} 

		#get exposure distribution for the current population, calculates both baseline and counterfactual data and stores in global attributes
		populationDistribution = PopDistributionRaw(DBHelperRaw.population_subsets,b_non_rate,b_mean,b_sd,c_non_rate,c_mean,c_sd,exposure_bins,dist_type)

		outcomes 	= {} # initialize all related outcomes for the current exposure in the loop below 
		o_ids 		= Set() # all ids of affected outcomes in current exposure
		for o_id in sorted(outcome_ids): # [related outcome id list]
			o_ids.add(o_id) # add current outcome id to the affected outcome list 
			mortality 	= mortalities.get(o_id) # mortality array, same size as population subsets, it can be from either database or previous exposure
			outcome_risks	= risks.get(o_id) 	# risks specific to outcome. Return an array where each index defines an specific risks for outcome
			name 		= DBHelperRaw.get_outcome_name(o_id) # outcome name
			lle 		= DBHelperRaw.exposure_outcome.get(e_id).get(o_id).get('lower_limit_estimate') # lower limit estimate
			ule 		= DBHelperRaw.exposure_outcome.get(e_id).get(o_id).get('upper_limit_estimate') # upper limit estimate
			measure 	= DBHelperRaw.exposure_outcome.get(e_id).get(o_id).get('measure') # measurements 
			outcome 	= PrimeOutcomeRaw(name,o_id,e_id,mortality,exposure_bins_rr,outcome_risks,lle,ule,measure) # initiate an outcome object
			outcomes[o_id] 	= outcome # add current outcome to current exposure outcomes list

		compound_outcome_ids 	= pre_compound_outcome_ids.union(o_ids) # compound outcome ids for recording which outcomes are affected by compound exposures
		exposure 		= PrimeExposureRaw(e_id,outcome_ids,compound_outcome_ids,mortalities,exposure_bins_rr,exposure_bins,outcomes,populationDistribution) # initiate an exposure object 
		return exposure

	def get_exposure_list(self, e_list):
    		"""This function, could be compound result or 'only' result, take a list as parameter, the list can have only one exposure parameter setting or multiple exposures parameter settings.

    		:param e_list: a list of exposure attributions[id:{mean_list,sd_list,non_rate_list}], if list is [4], then it is only sheet; if list is [1,2,3,4], then it is none sheet
    		:type e_list: list
   	 	:returns: a list of initial/baseline exposures 
    		"""
		if e_list == None: return # no changing
		self.cc_exposures 	= [] # could be compound result or 'only' result
		c_mortalities 		= DBHelperRaw.mortalities # this is the orginal mortality data for chosen population from database. This is to be used as initial mortalities for outcomes. 

		for e in e_list:
		 	e_id 		= int(e.get('e_id')) # exposure id, when get exposure id from database, it is a unicode
			outcome_ids     = DBHelperRaw.exposure_outcome.get(e_id) # {exposure_id:[related outcome ids]}
			if len(self.cc_exposures) > 0: # pre existed previous exposure
				pre_compound_outcome_ids = self.cc_exposures[-1].compound_outcome_ids 
			else: # the current exposure is the first exposure in the list
				pre_compound_outcome_ids = Set() 
			measurement	= DBHelperRaw.measurements.get(e_id) # [baseline mean, counterfactual mean, baseline sd, counterfactual sd, baseline non rate, counterfactual non rate]
			b_mean 		= measurement[0] 
			b_sd 		= measurement[2] 
			if len(measurement) > 4: # there are non rates parameters
				b_non_rate 	= measurement[4] 
			else: # there are not non rates parameters
				b_non_rate 	= None 
			list_size 	= len(b_mean)
			if e_id == 5: # for fat, we get parameters like total fat mean etc, we need to calculate cholestrol mean and cholestrol sd based on different fats parameters
				c_mean_total	= float(e.get('mean_total')) # total fat
				c_mean_sat	= float(e.get('mean_sat')) # saturated fat
				c_mean_mufa	= float(e.get('mean_mufa')) # mufa
				c_mean_pufa	= float(e.get('mean_pufa')) # pufa
				c_mean_diet	= float(e.get('mean_diet')) # dietary cholestrol

				c_sd_total	= float(e.get('sd_total')) # total fat
				c_sd_sat	= float(e.get('sd_sat')) # saturated fat
				c_sd_mufa	= float(e.get('sd_mufa')) # mufa
				c_sd_pufa	= float(e.get('sd_pufa')) # pufa
				c_sd_diet	= float(e.get('sd_diet')) # dietary cholestrol

				c_fat_means	= [c_mean_total,c_mean_sat,c_mean_mufa,c_mean_pufa,c_mean_diet] # stored in a array to transfer as one parameter, make the calculation function more expandable
				c_fat_sds	= [c_sd_total,c_sd_sat,c_sd_mufa,c_sd_pufa,c_sd_diet]

				c_mean_value	= get_balanced_mean(c_fat_means) # decimal value
				c_sd_value	= get_balanced_sd(c_fat_sds) # decimal value
				c_non_rate_value= None 
				# generate lists of mean and sd
				c_mean 		= generate_list_value(c_mean_value,list_size)
				c_sd 		= generate_list_value(c_sd_value,list_size)
			elif e_id == 7: # for bmi, we get calculate counterfactual mean using counterfactual met data and baseline mean  
				c_energy_mean 	= float(e.get('energy_mean')) # counterfactual mean for energy intake
				c_sedentary_rate= float(e.get('sedentary_rate'))
				c_met_mean 	= float(e.get('met_mean'))
				# c_met_sd 	= float(e.get('met_sd'))
				c_met_mvpa 	= float(e.get('met_mvpa'))
				c_met_non_mvpa 	= float(e.get('met_non_mvpa'))

				c_mean_value_m	= get_bmi_counterfactual_mean(float(DBHelperRaw.b_bmi_mean), float(DBHelperRaw.b_energy_mean), float(c_energy_mean), float(DBHelperRaw.b_height_mean), float(DBHelperRaw.b_sedentary_rate), float(DBHelperRaw.b_met_mean), float(DBHelperRaw.b_met_mvpa), float(DBHelperRaw.b_met_non_mvpa), float(c_sedentary_rate), float(c_met_mean), float(c_met_mvpa), float(c_met_non_mvpa), True)
				c_mean_value_f	= get_bmi_counterfactual_mean(float(DBHelperRaw.b_bmi_mean), float(DBHelperRaw.b_energy_mean), float(c_energy_mean), float(DBHelperRaw.b_height_mean), float(DBHelperRaw.b_sedentary_rate), float(DBHelperRaw.b_met_mean), float(DBHelperRaw.b_met_mvpa), float(DBHelperRaw.b_met_non_mvpa), float(c_sedentary_rate), float(c_met_mean), float(c_met_mvpa), float(c_met_non_mvpa), False)
				c_sd_value	= float(DBHelperRaw.b_bmi_sd) 
				c_non_rate_value= None 
				# generate lists of mean and sd, for bmi, male and female mean is different, this causes the difference of log mean and log sd
				half_list_size  = list_size/2
				c_mean 		= generate_list_value(c_mean_value_m,half_list_size) + generate_list_value(c_mean_value_f,half_list_size) # bmi means for men and woman are different 
				c_sd 		= generate_list_value(c_sd_value,list_size) 
			else:	# all other exposures
				c_mean_value	= float(e.get('mean'))
				c_sd_value	= float(e.get('sd'))
				c_non_rate_value= float(e.get('non_rate'))
				# generate lists of mean and sd
				c_mean 		= generate_list_value(c_mean_value,list_size)
				c_sd 		= generate_list_value(c_sd_value,list_size)

			# counterfactual non rate could possibly not exist
			if c_non_rate_value != None:
				c_non_rate 	= generate_list_value(c_non_rate_value,list_size)
			else: 
				c_non_rate 	= None 
			dist_type	= DBHelperRaw.exposures.get(e_id).get('dist_type') # unicode
			exposure 	= self.get_exposure(e_id,b_mean,b_sd,c_mean,c_sd,b_non_rate,c_non_rate,dist_type,c_mortalities,outcome_ids,pre_compound_outcome_ids)
			self.cc_exposures.append(exposure) # current counterfactual exposures
			c_mortalities 	= exposure.c_mortalities # counterfactual mortality for next exposure, unless the loop comes to the end
		
	def get_initial_exposures(self):
    		"""get the initial baseline and counterfactual exposures,*be called only once when the program started*, only_exposures keeps the same in the whole process, while cc_exposures changes with new parameters

    		:param self: self attrubtes 
   	 	:returns: a list of initial/baseline exposures 
    		"""
		self.only_exposures 	= {} # list of PrimeExposure objects
		keys 			= DBHelperRaw.exposures.keys()
		for e_id in keys: # get a list of exposures 
			exposure	= DBHelperRaw.exposures.get(exposure_id)	
			outcome_ids 	= DBHelperRaw.exposure_outcome.get(e_id)

			exposure_bins_rr= DBHelperRaw.exposure_bins_rr.get(e_id)
			exposure_bins 	= DBHelperRaw.exposure_bins.get(e_id)
			risks 		= DBHelperRaw.risks.get(e_id)
			dist_type   	= exposures.get('dist_type')
			b_mean 		= DBHelperRaw.measurements.get(e_id)[0]# [[b_means],[c_means],[b_sd],[c_sd],[b_non_rate],[c_non_rate]]
			c_mean 		= DBHelperRaw.measurements.get(e_id)[1] 
			b_sd 		= DBHelperRaw.measurements.get(e_id)[2] 
			c_sd 		= DBHelperRaw.measurements.get(e_id)[3] 
			if len(DBHelperRaw.measurements)<6: # some exposures have no non_rate, such as Fibre and Fats
				non_rate= genearte_list_value(0,len(b_mean)) # all value should be 0 
			else:	# some exposures have non_rate, such as fruit veg etc. 
				non_rate= DBHelperRaw.measurements.get(e_id)[4]
			mortalities	= DBHelperRaw.mortalities
			exposure 	= self.get_exposure(e_id,b_mean,b_sd,c_mean,c_sd,b_non_rate,c_non_rate,dist_type,c_mortalities,outcome_ids,outcome_ids)
			self.only_exposures[e_id] = exposure # add into current only_exposures list

	def get_counterfactual_compound_exposures(self, e_list):
    		"""get new counterfactual exposures, the e_list should be in the format of a list of dictionaries, e.g. [{'mean':1,'sd':0.5,'non_rate':0,'e_id':1},{}], *be called once a change is made*

    		:param e_list: a list of exposure parameters 
   	 	:returns: a list of counterfactual compound exposures, all these exposures are stored in the global variable cc_exposures, which can be called via self.cc_exposures 
    		"""
		self.get_exposure_list(e_list) # initiate attribute cc_exposures
		self.refresh_output_counterfactual_mortality() # refresh final compound mortality

	def refresh_output_baseline_mortality(self):
    		""" refresh final baseline compound mortality for output, it should be the baseline mortality of the intial exposure

    		:param self: self attrubtes 
   	 	:returns: No return
    		"""
		self.output_total_death_baseline	= DBHelperRaw.total_mortality
		self.output_baseline_mortality_num 	= DBHelperRaw.outcome_mortality
	
	def refresh_output_counterfactual_mortality(self):
    		""" refresh final compound mortality for output, it should be the counterfactual mortality of the final exposure.
		    	In order to show mortality by age/outcome/gender, there should be three lists.
		   	1. Show by age/population_subset 
				All information to present on a webpage is stored in variable 'output_all_mortality_exposure_age', the format of this variable is [{'population_subset_id':1,'age_group':'15-19','b_mortality_sum_db':757,'c_mrtality_sum':341}] 
		   	2. Show by outcome 
				All information to present on a webpage is stored in variable 'output_all_mortality_exposure_outcome', the format of this variable is [{'o_id':1,'name':'Stroke','b_mortality_sum_db':24757,'c_mrtality_sum':23415}] 
		   	3. Show by gender 
				All information to present on a webpage is stored in variable 'output_all_mortality_exposure_gender', the format of this variable is [{'gender':'male','b_mortality_sum_db':24757,'c_mrtality_sum':415}] 

    		:param self: self attrubtes 
   	 	:returns: No return
    		"""
		try:
			self.output_counterfactual_mortality 	= {} # a list of attributions that are to be shown in the webpage interface 
			if len(self.cc_exposures) < 1: #there is none combined counterfactual exposures
				return	
			exposure = self.cc_exposures[-1] # the last exposure in the compound exposures
			if None != exposure:
				self.output_counterfactual_mortality 	= exposure.c_mortalities # same format as original baseline mortality 
				self.output_counterfactual_mortality_num= [] # total mortality numbers for all exposures 
				for o_id in self.output_counterfactual_mortality:
					arr_deaths = self.output_counterfactual_mortality.get(o_id) # all population subset deaths for one outcome 
					self.output_counterfactual_mortality_num.append(sum(arr_deaths))  # add into outcomes mortality number list
				#sum of all outcome all population subsets deaths
				self.output_counterfactual_mortality_total = sum(self.output_counterfactual_mortality_num) 
				self.output_total_death_averted		= DBHelperRaw.total_mortality - self.output_counterfactual_mortality_total # total death averted by counterfactual parameters 
			self.output_all_mortality_exposure_outcome 	= [] # content to present in a website interface or other conditions, dictionary of outcomes
			self.output_all_mortality_age			= [] # dictionary of ages
			self.output_all_mortality_gender 		= [] # dictionary of gender 
			# get infomation of mortalities to present 
			for o_id in exposure.compound_outcome_ids:

				# output information for outcomes 
				mortality_detail_outcome 			= {} # one mortality detail for one outcome
				mortality_detail_outcome['o_id'] 		= o_id  # outcome id
				mortality_detail_outcome['name'] 		= DBHelperRaw.get_outcome_name(o_id) # outcome name
				mortality_detail_outcome['b_mortality_sum_db'] 	= DBHelperRaw.outcome_mortality.get(o_id) # baseline mortality from database
				mortality_detail_outcome['c_mortality_sum'] 	= exposure.c_mortalities_outcome.get(o_id) #final counterfactual mortality for compound exposures
				self.output_all_mortality_exposure_outcome.append(mortality_detail_outcome) # data to represent in the interface, left-hand side
				
				# output information for ages
				if len(self.output_all_mortality_age) < 1:
					for i in xrange(1,DBHelperRaw.age_group_num + 1): # i is the age group id
						mortality_detail_age				= {} # one mortality detail for one age group 
						mortality_detail_age['population_subset_id']	= i # age group id 
						mortality_detail_age['age_group']		= DBHelperRaw.get_age_group(i-1) # age group name
						mortality_detail_age['b_mortality_sum_db'] 	= DBHelperRaw.age_mortality.get(i) # baseline mortality from database
						mortality_detail_age['c_mortality_sum'] 	= exposure.c_mortalities_age.get(i) # final counterfactual mortality for compound exposures
						self.output_all_mortality_age.append(mortality_detail_age)
				else:
					for i in xrange(1,DBHelperRaw.age_group_num + 1): # i is the age group id
						mortality_detail_age				= self.output_all_mortality_age[i-1] # one mortality detail for one age group 
						mortality_detail_age['c_mortality_sum'] 	= exposure.c_mortalities_age.get(i) # final counterfactual mortality for compound exposures
						self.output_all_mortality_age[i-1] 		= mortality_detail_age

			mortality_detail_male				= {} # one mortality detail for one outcome
			mortality_detail_male['gender'] 		= 'male' # outcome id
			mortality_detail_male['b_mortality_sum_db'] 	= DBHelperRaw.gender_mortality.get('male') # baseline mortality from database
			mortality_detail_male['c_mortality_sum'] 	= exposure.c_mortalities_gender.get('male') # final counterfactual mortality for compound exposures

			mortality_detail_female				= {} # one mortality detail for one outcome
			mortality_detail_female['gender'] 		= 'female' # outcome id
			mortality_detail_female['b_mortality_sum_db'] 	= DBHelperRaw.gender_mortality.get('female') # baseline mortality from database
			mortality_detail_female['c_mortality_sum'] 	= exposure.c_mortalities_gender.get('female') # final counterfactual mortality for compound exposures

			self.output_all_mortality_gender.append(mortality_detail_male)
			self.output_all_mortality_gender.append(mortality_detail_female)
			
		except IOError as e:
    			print "I/O error({0}): {1}".format(e.errno, e.strerror)

	def get_attr_cc_exposure(self,index):
    		"""get the i_th exposure in counterfactual compound exposures list, all exposures mortalities are the compound results of all previous exposures. The mortality of the first exposure is the same as baseline only exposure mortality, in any case of future use.

    		:param index: index of exposure 
    		:type index: int 
   	 	:returns: the indexth exposure, an PrimeExposure object 
   	 	:raises: index out of bound error 
    		"""
		try:
			exposures = self.cc_exposures
			if len(exposures) < 1: return
			return exposures[index]
		except ValueError:
			print 'Index out of bound' 

	def get_attr_exposure_outcome_death_gender(self, index, o_id):
    		"""get ith exposure o_id th death from new counterfactual exposures, this is useful when user click 'show by age'

    		:param index: index of exposure 
    		:type index: int 
    		:param o_id: outcome id, the same id as in the database 
    		:type a_id: int 
    		:param is_male: gender 
    		:type is_male: bool 
    		:param is_baseline: is baleline or counterfactual 
    		:type is_baseline: bool 
   	 	:returns: [b_m,b_f,c_m,c_f]death sum for a specific exposure and outcome 
    		"""
		exposure 	= self.cc_exposures[index]
		b_m		= sum(exposure.outcomes.get(o_id).mortality[:15])
		b_f		= sum(exposure.outcomes.get(o_id).mortality[15:])
		c_m		= sum(exposure.outcomes.get(o_id).c_mortality[:15])
		c_f		= sum(exposure.outcomes.get(o_id).c_mortality[15:])
		return [b_m,b_f,c_m,c_f] 

	def get_attr_b_exposure_outcome_death(self, index, o_id):
    		"""get ith exposure o_id th death from baseline exposures

    		:param index: index of exposure 
    		:type index: int 
    		:param o_id: outcome id, the same id as in the database 
    		:type a_id: int 
   	 	:returns: death sum for a specific exposure and outcome in baseline case 
    		"""
		exposure 		= self.only_exposures[index]
		outcomes_deaths_sum 	= exposure.get_outcome_deaths_sum(o_id,True)
		return outcomes_deaths_sum

	#################################################
	# deaths according to age 
	#################################################
	def get_attr_b_death_age(self, a_id):
    		"""get deaths for a_id age group for all exposures [baseline]

    		:param a_id: age group id 
    		:type a_id: int 
   	 	:returns: death sum for a specific age group in baseline 
    		"""
		#if not DBHelperRaw.is_agegroup_valid(a_id): return -1
		age_deaths_sum = 0
		only_exposures = self.only_exposures
		for i in self.only_exposures:
			exposure 	= self.only_exposures.get(i)
			deaths 		= self.get_exposure_outcome_death_age(a_id, exposure)
			age_deaths_sum += deaths
		return age_deaths_sum

	def get_attr_c_death_age(self, a_id):
    		"""get deaths for a_id age group for all *initial* exposures [counterfactual]

    		:param a_id: age group id 
    		:type a_id: int 
   	 	:returns: death sum for a specific age group in counterfactual 
    		"""
		age_deaths_sum = 0
		for exposure in self.only_exposures:
			deaths 		= self.get_exposure_outcome_death_age(a_id, exposure)
			age_deaths_sum += deaths
		return age_deaths_sum

	def get_attr_cc_death_age(self, a_id):
    		"""get deaths for a_id age group for all *new* exposures [counterfactual][compound]

    		:param a_id: age group id 
    		:type a_id: int 
   	 	:returns: death sum for a specific age group in changed counterfactual 
    		"""
		age_deaths_sum = 0
		for exposure in self.cc_exposures:
			deaths 		= self.get_exposure_outcome_death_age(a_id, exposure)
			age_deaths_sum += deaths
		return age_deaths_sum

	def get_attr_b_exposure_outcome_death_age(self, index, a_id):
    		"""get indexth exposure deaths for a_id age group [baselie]

    		:param index: index of exposure 
    		:type index: int 
    		:param a_id: age group id 
    		:type a_id: int 
   	 	:returns: death sum for a specific age group and a specific exposure in baseline 
    		"""
		exposure 	= self.only_exposures[index]
		age_deaths_sum 	= self.get_exposure_outcome_death_age(a_id,exposure)
		return age_deaths_sum

	def get_attr_c_exposure_outcome_death_age(self, index, a_id):
    		"""get indexth exposure deaths for a_id age group [counterfactual]

    		:param index: index of exposure 
    		:param a_id: age group id 
    		:type a_id: int 
   	 	:returns: death sum for a specific age group and a specific exposure in counterfactual 
    		"""
		exposure 	= self.cc_exposures[index]
		age_deaths_sum 	= self.get_exposure_outcome_death_age(a_id,exposure)
		return age_deaths_sum

	def get_exposure_outcome_death_age(self, a_id, exposure):
    		"""get deaths sum for a_id age group in exposure, this age group id (a_id) should be a valid id for exposure, otherwise it raises NotFound or IndexOutOfBound error

    		:param a_id: age group id 
    		:type a_id: int 
    		:param exposure: exposure to get data 
    		:type exposure: an PrimeExposure object 
   	 	:returns: deaths sum for a_id age group
    		"""
		age_deaths_e	= 0
		age_deaths_e 	= exposure.get_age_deaths_sum(a_id) #death sum for one exposure 
		#return age_deaths_sum
		return age_deaths_e
		
		
