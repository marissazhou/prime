"""dabatabase manipulation class
.. module:: DBHelper 
   :platform: Ubuntu Unix
   :synopsis: A module for conducting all database relavant manipulations.

.. moduleauthor:: Lijuan Marissa Zhou <marissa.zhou.cn@gmail.com>

"""
from primemodel.models import *
from primemodel.prime import *
from primemodel.logic import *
import unicodedata

class DBHelper: 
	
	relative_risks 		= None
	population_subsets 	= None
	measurements 		= None
	
	outcomes_num 		= 24 # 24 types of outcomes 
	age_group_num		= 0  # age group number 
	population_subsets	= {} 
	population_total_size	= 0 
	total_mortality		= 0 
	outcome_mortality	= {}  # each element is the baseline sum mortality for each outcome for all age groups
	age_mortality		= {}  # each element is the baseline sum mortality for each age for all outcomes 
	gender_mortality	= {}  # each element is the baseline sum mortality for each gender for all age groups and outcome
	
	#mortalities in database
	mortalities 		= {} 
	exposure_bins_rr	= {} # for relative risks
	exposure_bins 		= {} # for population 
	# initial risks referred to references, referred to database table primemodel_relativerisks 
	risks 			= {} 
	# all exposures, refer to database table primemodel_exposure
	exposures 		= {}
	outcomes 		= {} 
	# exposure_outcome relationship, including measures
	exposure_outcome 	= {} 

	@staticmethod
	def initialize():
		"""This function initializes an DBHelper instance 

    		:param : 
   	 	:returns: 
    		"""
		DBHelper.get_exposures()
		DBHelper.get_exposure_outcome()
		DBHelper.get_relative_risks()
		DBHelper.get_population_subsets(1)
		DBHelper.get_measurements()
		DBHelper.get_outcomes()
		DBHelper.get_mortalities()
		DBHelper.get_samples() # for population and relative risks
		DBHelper.get_risks()
		DBHelper.get_bmi_measurements()

	@staticmethod
	def get_samples():
		"""This function returns all samples for outcomes of all exposures 

    		:param : 
   	 	:returns: No return 
    		"""
		DBHelper.exposure_bins_rr = {}
		DBHelper.exposure_bins = {}
		# all exposures
		for e_id in DBHelper.exposures:
			#exposure id
			rr_bins		= []
			pop_bins	= []
			# related outcome risks
			rr_bins_values 	= ExposureBins.objects.filter(exposure=e_id,bin_type='r').values('bin_value')
			pop_bins_values = ExposureBins.objects.filter(exposure=e_id,bin_type='p').values('bin_value')
			for i in range(len(rr_bins_values)):
				rr_bins.append(float(rr_bins_values[i].get('bin_value')))
				pop_bins.append(float(pop_bins_values[i].get('bin_value')))
			DBHelper.exposure_bins_rr[e_id] = rr_bins
			DBHelper.exposure_bins[e_id] 	= pop_bins


	@staticmethod
	def get_risks():
		"""This function returns all baseline risks for all exposures 

    		:param : 
   	 	:returns: No return 
    		"""
		DBHelper.risks = {}
		
		#get risks from database table primemodel_relativerisks
		# all exposures
		for e_id in DBHelper.exposures:#exposure id
			# related outcome ids
			e_o = DBHelper.exposure_outcome
			outcome_ids = DBHelper.exposure_outcome.get(e_id)
			# related outcome risks
			risks_outcomes= {}
			for o_id in outcome_ids:
				# get data from database
				exposureoutcome_risks = RelativeRisk.objects.filter(exposure=e_id,outcome=o_id).order_by('population_subset','id').values('risk_value')
				# add into risks list of current exposure
				o_risks = []
				length = len(exposureoutcome_risks)
				for i in range(length):
					o_risks.append(float(exposureoutcome_risks[i].get('risk_value')))	
				risks_outcomes[o_id] = o_risks
			# add into risks lists of all exposures
			DBHelper.risks[e_id] = risks_outcomes

	@staticmethod
	def get_relative_risks():
		"""This function retrieves all relative risks from database, exposures store in a datastructure of [{}] 

    		:param : 
   	 	:returns: No return 
    		"""
		relative_risks = ExposureDistribution.objects.all()
	
	@staticmethod
	def get_relative_risks_count():
		"""This function retrieves all exposure distribution from database, exposures store in a datastructure of [{}] 

    		:param : 
   	 	:returns: No return 
    		"""
		relative_risks_count = ExposureDistribution.objects.count() 
		return relative_risks_count
	
	
	#@staticmethod
	#def get_population_subsets():
	#	"""This function retrieves all population subsets from database, exposures store in a datastructure of [] 
#
#    		:param : 
#   	 	:returns: No return 
#    		"""
#		population_subsets = PopulationSubset.objects.all().order_by('created_at')
#		return population_subsets 

	@staticmethod
	def get_population_subsets(pop_id):
		"""This function retrieves population subsets from database, exposures store in a datastructure of [] 

    		:param pop_id: population id 
   	 	:returns: female age groups 
    		"""
		DBHelper.population_total_size 	= 0	
		population_subsets 		= PopulationSubset.objects.filter(population_id=pop_id).order_by('id').values('age_group','gender','size')
		for subset in population_subsets:
			DBHelper.population_total_size  += subset.get('size')	
		DBHelper.population_subsets	= population_subsets
		DBHelper.age_group_num		= len(DBHelper.population_subsets)

	@staticmethod
	def get_age_group(age_group_id):
		"""This function return age group according to age group id 

    		:param : 
   	 	:returns: No return 
    		"""
		age_group = DBHelper.population_subsets[age_group_id].get('age_group')
		return age_group

	@staticmethod
	def get_measurements():
		"""This function retrieves all measurements from database, exposures store in a datastructure of {[]} 

    		:param : 
   	 	:returns: No return 
    		"""
		DBHelper.measurements = {}
		try:
			for exposure_id in DBHelper.exposures:
				#exposure_id = exposure.get('id')
				DBHelper.measurements[exposure_id] = DBHelper.get_measurements_lists(exposure_id)#[[b_means],[c_means],[b_sds],[c_sds],[b_non_rates],[c_non_rates]]
		except (IndexError,TypeError,ValueError,NameError) as e: 	
			print "Error({0}): {1}".format(e.strerror)
			
	@staticmethod
	def get_bmi_measurements():
		"""This function retrieves all measurements bmi 

    		:param : 
   	 	:returns: No return 
    		"""
		DBHelper.b_bmi_mean = DBHelper.get_bmi_mean()
		DBHelper.b_bmi_sd = DBHelper.get_bmi_sd() 
		DBHelper.b_energy_mean = DBHelper.get_bmi_energy_total() 
		DBHelper.b_height_mean = DBHelper.get_bmi_height() 
		DBHelper.b_sedentary_rate = DBHelper.get_sedentary_rate() 
		DBHelper.b_met_mean = DBHelper.get_met_mean()
		DBHelper.b_met_mvpa = DBHelper.get_met_mvpa()
		DBHelper.b_met_non_mvpa = DBHelper.get_met_non_mvpa()
		
	@staticmethod
	def get_measurements_lists(exposure_id):
		"""This function retrieve all measurements for one exposure 

    		:param m_type_ids: measurement type id 
    		:type m_type_ids: list 
   	 	:returns: measurement list for one exposure 
    		"""
		lists = [] #list of one exposure mean/sd/non-rates, [baseline mean, counterfactual mean, baseline sd, counterfactual sd, baseline non rate, counterfactual non rate], for fats, it could be [baseline total fat mean, counterfactual total fat mean, baseline saturate fat mean, counterfactual saturate fat mean, ...]

		mean_ids 	= DBHelper.get_measurement_type_id(exposure_id, 'Mean')
		sd_ids 		= DBHelper.get_measurement_type_id(exposure_id, 'SD')
		percentage_ids 	= DBHelper.get_measurement_type_id(exposure_id, 'Percentage') #could be empty list
		measuretype_ids = mean_ids + sd_ids + percentage_ids

		for measuretype_id in measuretype_ids : #measuretype_ids is in the format of [{'id':1},{'id':2}]
			if measuretype_id != None:
				lists.append(DBHelper.get_measurements_list(measuretype_id,True)) #baseline measurements
				lists.append(DBHelper.get_measurements_list(measuretype_id,False)) #counterfactual measurements

		# for fat exposure, the mean and sd should be transered into cholestrol measurements
		if exposure_id == 5: #list size is 20, in the form of [b_mean_total_fat, c_mean_total_fat, ...]
			# the following four are means sd and non rate for fats 
			b_mean 		= []
			b_sd		= []
			c_mean 		= []
			c_sd		= []

			length_list 	= len(lists)
			length_row 	= len(lists[0])
			for i in range(length_row): #for each population subset, calculate cholestrol mean and sd based on different fats mean and sd 
				b_fat_means 	= [] # baseline fats means
				b_fat_sds	= []
				c_fat_means 	= []
				c_fat_sds	= []
				fat_num 	= length_list/4
				space		= length_list/2
				for j in range(fat_num): #means 
					index_start = j*2 # index for baseline mean
					b_fat_means.append(lists[index_start][i]) # baseline means for fats
					c_fat_means.append(lists[index_start+1][i]) # counterfactual means for fats
					b_fat_sds.append(lists[index_start+space][i]) # baseline sd for fats
					c_fat_sds.append(lists[index_start+1+space][i]) # counterfactual sd for fats

				b_mean_one_value= get_balanced_mean(b_fat_means) # decimal value
				c_mean_one_value= get_balanced_mean(c_fat_means) # decimal value
				b_sd_one_value	= get_balanced_sd(b_fat_sds) # decimal value
				c_sd_one_value	= get_balanced_sd(c_fat_sds) # decimal value

				b_mean.append(b_mean_one_value) 
				c_mean.append(c_mean_one_value) 
				b_sd.append(b_sd_one_value) 
				c_sd.append(c_sd_one_value) 

			lists = [b_mean,c_mean,b_sd,c_sd] #[baseline cholestrol mean, counterfactual cholestrol mean, baseline cholestrol sd, counterfactual cholestrol sd]

		# for bmi exposure, the energy intake and height are not considered at the moment 
		if exposure_id == 7: #list size is 8, in the form of [b_mean_energy_intake, c_mean_energy_intake, ...]
			lists = lists[4:-1]

		return lists # in the format of [baseline mean, counterfactual mean, baseline sd, counterfactual sd, baseline non rate, counterfactual non rate]

	@staticmethod
	def get_measurements_list(m_type_id, is_baseline):
		"""This function retrieves all measurements from database, exposures store in a datastructure of {[]} 

    		:param m_type_id: measurement type id 
    		:type m_type_id: int 
    		:param is_baseline: True is baseline, false is counterfactual 
    		:type is_baseline: bool 
   	 	:returns: measurement list for one measurement type baseline or counterfactual 
    		"""
		values = []
		if is_baseline:
			measurements = Measurement.objects.filter(measurement_type_id=m_type_id,measurement_option='B').order_by('population_subset').values('value')
		else:
			measurements = Measurement.objects.filter(measurement_type_id=m_type_id,measurement_option='C').order_by('population_subset').values('value')
		# only get number value
		for m in measurements:
			values.append(float(m.values()[0])) 
		return values

 	#select * from primemodel_measurement where measurement_type_id= (select id from primemodel_measurementtype where exposure_id=1 and statistical_measure='Mean');
	@staticmethod
	def get_measurement_type_id(e_id, statistical_measure_type):
		"""This function retrieves the measurement type id for a specific measurement like mean of fibre 
    		:param e_id: exposure id 
    		:type e_id: int 
    		:param is_baseline: True is baseline, false is counterfactual 
    		:type is_baseline: bool 
   	 	:returns: one specific measurement type id or id list accroding to what the exposure_id is, like if exposure is alchohol, exposure_id is 9, then it returns a list of measurement type id, and it can be also empty like percentage for fibre consumers 
    		"""
		ids = MeasurementType.objects.filter(exposure_id=e_id,statistical_measure=statistical_measure_type).order_by('id').values('id')
		ids_num = []
		if ids != None:
			for i in ids:
				ids_num.append(i.get('id'))	
		return ids_num

	@staticmethod
	def get_mortalities():
		"""This function retrieves all mortalities from database, exposures store in a datastructure of {} 

    		:param : 
   	 	:returns: No return 
    		"""
		DBHelper.mortalities 	= {} # {outcome_id: outcome} 
		DBHelper.total_mortality=0
		keys 			= DBHelper.outcomes.keys()

		# outcome mortality
		for i in DBHelper.outcomes.keys():
			mortality 		= Mortality.objects.filter(outcome=i).order_by('population_subset').values('value')
			mortality_nums 	= [] # mortality for one outcome
			for m in mortality:
				m_value = int(m.values()[0]) 
				mortality_nums.append(m_value) 
			sum_mortality_outcome = sum(mortality_nums)
			DBHelper.outcome_mortality[i] 	= sum_mortality_outcome # add into outcome mortality sum list	
			DBHelper.total_mortality 	= DBHelper.total_mortality + sum_mortality_outcome # add up to total baseline mortality 
			DBHelper.mortalities[i]  	= mortality_nums 

		age_group_separator 	= DBHelper.age_group_num/2 + 1 
		sum_mortality_male 	= 0# add into gender mortality sum list	
		sum_mortality_female 	= 0# add into gender mortality sum list	
		# age and gender mortality
		for i in xrange(1,DBHelper.age_group_num + 1):
			mortality 	= Mortality.objects.filter(population_subset_id=i).order_by('outcome').values('value')
			mortality_nums 	= [] # mortality for one outcome
			for m in mortality:
				m_value = int(m.values()[0]) 
				mortality_nums.append(m_value) 
			sum_mortality_age= sum(mortality_nums)
			if i < age_group_separator: # male
				sum_mortality_male 	= sum_mortality_male + sum_mortality_age # add up to gender mortality sum 
			else: # female
				sum_mortality_female 	= sum_mortality_female + sum_mortality_age # add up to gender mortality sum 
			DBHelper.age_mortality[i] 	= sum_mortality_age # add into age mortality sum list	

		DBHelper.gender_mortality['male'] 		= sum_mortality_male # add into gender mortality sum list	
		DBHelper.gender_mortality['female']		= sum_mortality_female # add into gender mortality sum list	

	@staticmethod
	def get_exposures():
		"""This function retrieves all exposures from database, exposures store in a datastructure of [{}] 

    		:param : 
   	 	:returns: all exposures in database 
    		"""
		exposures = Exposure.objects.all().order_by('id').values('id','name','dist_type')
		DBHelper.exposures = {} 
		for e in exposures:
			e_id = int(e.get('id'))	
			DBHelper.exposures[e_id] = {'name':str(e.get('name')),'dist_type':int(e.get('dist_type'))} # all data fetched from database are in form of unicode 
		return DBHelper.exposures

	@staticmethod
	def get_outcomes():
		"""This function retrieves all outcomes from database, outcome store in a datastructure of {o_id:[name,abbreviation]} 

    		:param : 
   	 	:returns: No return 
    		"""
		outcomes= Outcome.objects.all().order_by('id').values('id','name','abbreviation')
		for outcome in outcomes:
			o_id			= int(outcome.get('id'))
			name 			= outcome.get('name')
			name 			= unicodedata.normalize('NFKD', name).encode('ascii','ignore')
			abbreviation 		= outcome.get('abbreviation')
			DBHelper.outcomes[o_id]	= [name,abbreviation] 
		
		return DBHelper.outcomes

	@staticmethod
	def get_exposure_id(e_id):
		"""This function return exposure id according to exposure id 

    		:param abbreviation: outcome abbreviation 
    		:type abbreviation: string 
   	 	:returns: outcome id 
    		"""
		exposure_id = DBHelper.exposures[e_id-1].get('id')
		return exposure_id

	@staticmethod
	def get_exposure_id_from_name(exposure_name):
		"""This function return exposure id according to exposure name 

    		:param exposure_name: exposure name 
    		:type exposure_name: string 
   	 	:returns: exposure id 
    		"""
		for eid in DBHelper.exposures:
			if exposure_name == DBHelper.exposures[eid].get('name'):
				return eid
		return None 

	@staticmethod
	def get_exposure_outcome():
		"""This function stores outcomes into database, exposure_outcome={exposure_id:}

    		:param : 
   	 	:returns: No return 
    		"""
		DBHelper.exposure_outcome = {} 
		# fetch data from database
		exposures 	= ExposureOutcome.objects.all().order_by('id').values('exposure','outcome','lower_limit_estimate','upper_limit_estimate','measure')
		# store data into an easy-to-search data format 
		outcome_ids 	= {} 
		e_id 		= 1
		for e in exposures:
			new_e_id= int(e.get('exposure'))
			o_id 	= int(e.get('outcome'))
			lle 	= e.get('lower_limit_estimate')
			ule 	= e.get('upper_limit_estimate')
			measure = float(e.get('measure'))
			if new_e_id == e_id: #the same exposure
				outcome_ids[o_id] 		= {'lower_limit_estimate':lle,'upper_limit_estimate':ule,'measure':measure}#store in a dictionary
			else: #a new exposure
				DBHelper.exposure_outcome[e_id]	= outcome_ids; 
				outcome_ids 			= {} 
				outcome_ids[o_id] 		= {'lower_limit_estimate':lle,'upper_limit_estimate':ule,'measure':measure}#store in a dictionary
				#outcome_ids[o_id] 		= [lle,ule,float(measure)]
				e_id 				= new_e_id
		DBHelper.exposure_outcome[e_id] = outcome_ids #{e_id:{o_id:[lle,ule]}} 

	@staticmethod
	def get_compound_exposure_outcome_ids(e_ids):
		"""This function return all relavant outcome ids for all exposures in e_ids

    		:param e_id: random exposure ids composure 
    		:type e_ids: list 
   	 	:returns: all relavant outcome ids for all exposures in e_ids 
    		"""
		outcome_ids = {}
		for e_id in e_ids:
			e_outcome_ids = DBHelper.exposure_outcome[e_id] # all outcome_ids for one exposure,  {'lower_limit_estimate':lle,'upper_limit_estimate':ule,'measure':measure}#
			
	@staticmethod
	def get_outcome_name(o_id):
		"""This function return outcome name according to outcome id 

    		:param o_id: outcome id 
    		:type o_id: int 
   	 	:returns: outcome name 
    		"""
		return DBHelper.outcomes.get(o_id)[0]

	@staticmethod
	def get_outcome_abbreviation(o_id):
		"""This function return outcome abbreviation according to outcome id 

    		:param o_id: outcome id 
    		:type o_id: int 
   	 	:returns: outcome abbreviation 
    		"""
		return DBHelper.outcomes.get(o_id)[1]

	@staticmethod
	def get_outcome_id(abbreviation):
		"""This function return outcome id according to outcome abbreviation 

    		:param abbreviation: outcome abbreviation 
    		:type abbreviation: string 
   	 	:returns: outcome id 
    		"""
		o_id = 1
		for key in DBHelper.outcomes.keys():
			if abbreviation == DBHelper.outcomes.get(key)[1]:
				return key	
		return o_id

	@staticmethod
	def get_test_data_bunch():
		"""This function fetches all test data from database 

   	 	:returns: test data 
    		"""
		DBHelper.test_exposure_sequences = [] #[[{}]] 
		DBHelper.test_results = [] #[1,2,...] 
		# fetch data from database
		#test_parameters = TestParameter.objects.all().order_by('id')
		test_parameters = TestParameter.objects.all()

		for test_parameter in test_parameters:
			total_energy_mean 	= test_parameter.total_energy_mean
			fruit_mean 		= test_parameter.fruit_mean
			fruit_sd		= test_parameter.fruit_sd
			fruit_non_rate		= test_parameter.fruit_non_rate
			veg_mean		= test_parameter.veg_mean
			veg_sd			= test_parameter.veg_sd
			veg_non_rate		= test_parameter.veg_non_rate
			fibre_mean		= test_parameter.fibre_mean
			fibre_sd		= test_parameter.fibre_sd
			salt_mean		= test_parameter.salt_mean
			salt_sd			= test_parameter.salt_sd
			total_fat_mean		= test_parameter.total_fat_mean
			total_fat_sd		= test_parameter.total_fat_sd
			saturate_fat_mean	= test_parameter.saturate_fat_mean
			saturate_fat_sd		= test_parameter.saturate_fat_sd
			mufa_fat_mean		= test_parameter.mufa_fat_mean
			mufa_fat_sd		= test_parameter.mufa_fat_sd
			pufa_fat_mean		= test_parameter.pufa_fat_mean
			pufa_fat_sd		= test_parameter.pufa_fat_sd
			dietary_cholesterol_mean= test_parameter.dietary_cholesterol_mean
			dietary_cholesterol_sd	= test_parameter.dietary_cholesterol_sd
			met_mean		= test_parameter.met_mean
			met_sd			= test_parameter.met_sd
			sedentary_rate		= test_parameter.sedentary_rate
			met_non_mvpa		= test_parameter.met_non_mvpa
			met_mvpa		= test_parameter.met_mvpa
			alcohol_low		= test_parameter.alcohol_low
			alcohol_mean		= test_parameter.alcohol_mean
			alcohol_sd		= test_parameter.alcohol_sd
			smoker_never		= test_parameter.smoker_never
			smoker_previous		= test_parameter.smoker_previous
			smoker_current		= test_parameter.smoker_current
			result			= test_parameter.result
	
			'''
			#bmi
			c_energy_mean = total_energy_mean 
			c_sedentary_rate = sedentary_rate
			c_met_mean = met_mean 
			c_met_mvpa = met_mvpa 
			c_met_non_mvpa = met_non_mvpa 
		
			bmi_mean = get_bmi_counterfactual_mean(float(DBHelper.b_bmi_mean), float(DBHelper.b_energy_mean), float(c_energy_mean), float(DBHelper.b_height_mean), float(DBHelper.b_sedentary_rate), float(DBHelper.b_met_mean), float(DBHelper.b_met_mvpa), float(DBHelper.b_met_non_mvpa), float(c_sedentary_rate), float(c_met_mean), float(c_met_mvpa), float(c_met_non_mvpa))
			bmi_sd   = float(DBHelper.b_bmi_sd)
			'''

			exposure_sequence = []
			exposure_sequence.append({u'non_rate': fruit_non_rate, 	u'e_id': 1, u'sd': fruit_sd, 	u'mean': fruit_mean}) #fruit 
			exposure_sequence.append({u'non_rate': veg_non_rate, 	u'e_id': 2, u'sd': veg_sd, 	u'mean': veg_mean}) #veg
			exposure_sequence.append({u'non_rate': 0, 		u'e_id': 3, u'sd': fibre_sd, 	u'mean': fibre_mean}) #fibre
			exposure_sequence.append({u'non_rate': 0, 		u'e_id': 4, u'sd': salt_sd, 	u'mean': salt_mean}) #salt
			exposure_sequence.append({u'non_rate': 0, 		u'e_id': 5, u'sd_total': total_fat_sd, 	u'mean_total': total_fat_mean, u'sd_sat': saturate_fat_sd, 	u'mean_sat': saturate_fat_mean, u'sd_mufa': mufa_fat_sd, 	u'mean_mufa': mufa_fat_mean, u'sd_pufa': pufa_fat_sd, 	u'mean_pufa': pufa_fat_mean, u'sd_diet': dietary_cholesterol_sd,	u'mean_diet': dietary_cholesterol_mean}) #fat
			exposure_sequence.append({u'non_rate': sedentary_rate, 	u'e_id': 6, u'sd': met_sd, 	u'mean': met_mean}) # physical activity
			exposure_sequence.append({u'sedentary_rate': sedentary_rate,u'e_id': 7,	u'energy_mean': total_energy_mean, u'met_mean': met_mean, 	u'met_mvpa': met_mvpa, u'met_non_mvpa':met_non_mvpa}) # bmi
			exposure_sequence.append({u'non_rate': alcohol_low, 	u'e_id': 8, u'sd': alcohol_sd, 	u'mean': alcohol_mean}) #alcohol
			exposure_sequence.append({u'non_rate': smoker_never, 	u'e_id': 9, u'sd': smoker_current, u'mean': smoker_previous}) #smoking

			# store data into an easy-to-search data format 
			DBHelper.test_exposure_sequences.append(exposure_sequence)#a new exposure sequence
			DBHelper.test_results.append(result)#all results in tests

	@staticmethod
	def get_bmi_energy_total():
		"""This function get baseline energy total for bmi 

   	 	:returns: energy_total
    		"""
		energies = Measurement.objects.filter(measurement_type_id=1,measurement_option='B').order_by('population_subset').values('value')
		energy_total = energies[0].get('value') #all energies value are same
		return energy_total

	@staticmethod
	def get_bmi_height():
		"""This function get baseline energy total for bmi 

   	 	:returns: energy_total
    		"""
		heights = Measurement.objects.filter(measurement_type_id=27,measurement_option='B').order_by('population_subset').values('value')
		height = heights[0].get('value')
		return height 

	@staticmethod
	def get_bmi_mean():
		"""This function get baseline energy total for bmi 

   	 	:returns: energy_total
    		"""
		means= Measurement.objects.filter(measurement_type_id=28,measurement_option='B').order_by('population_subset').values('value')
		mean = means[0].get('value')
		return mean 

	@staticmethod
	def get_bmi_sd():
		"""This function get baseline energy total for bmi 

   	 	:returns: energy_total
    		"""
		sds = Measurement.objects.filter(measurement_type_id=29,measurement_option='B').order_by('population_subset').values('value')
		sd = sds[0].get('value')
		return sd 

	@staticmethod
	def get_met_mean():
		"""This function get baseline energy total for bmi 

   	 	:returns: energy_total
    		"""
		met_means = Measurement.objects.filter(measurement_type_id=22,measurement_option='B').order_by('population_subset').values('value')
		met_mean = met_means[0].get('value')
		return met_mean 

	@staticmethod
	def get_sedentary_rate():
		"""This function get baseline energy total for bmi 

   	 	:returns: energy_total
    		"""
		rates = Measurement.objects.filter(measurement_type_id=24,measurement_option='B').order_by('population_subset').values('value')
		rate = rates[0].get('value')
		return rate 

	@staticmethod
	def get_met_non_mvpa():
		"""This function get baseline energy total for bmi 

   	 	:returns: energy_total
    		"""
		non_mvpas = Measurement.objects.filter(measurement_type_id=25,measurement_option='B').order_by('population_subset').values('value')
		non_mvpa = non_mvpas[0].get('value')
		return non_mvpa

	@staticmethod
	def get_met_mvpa():
		"""This function get baseline energy total for bmi 

   	 	:returns: energy_total
    		"""
		mvpas = Measurement.objects.filter(measurement_type_id=26,measurement_option='B').order_by('population_subset').values('value')
		mvpa = mvpas[0].get('value')
		return mvpa 
