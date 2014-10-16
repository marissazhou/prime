"""dabatabase manipulation class
.. module:: DBHelperRaw 
   :platform: Ubuntu Unix
   :synopsis: A module for conducting all database relavant manipulations.

.. moduleauthor:: Lijuan Marissa Zhou <marissa.zhou.cn@gmail.com>

"""
import logic
import unicodedata
import _mysql
import MySQLdb as mdb



class DBHelperRaw: 
	
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

	mortalities 		= {} #mortalities in database
	exposure_bins_rr	= {} # for relative risks
	exposure_bins 		= {} # for population 
	# initial risks referred to references, referred to database table primemodel_relativerisks 
	risks 			= {} 
	# all exposures, refer to database table primemodel_exposure
	exposures 		= {}
	outcomes 		= {} 
	# exposure_outcome relationship, including measures
	exposure_outcome 	= {} 
        con = mdb.connect('localhost', 'primeuser', 'primepass', 'prime')

	@staticmethod
	def initialize():
		"""This function initializes an DBHelperRaw instance 

    		:param : 
   	 	:returns: 
    		"""
		DBHelperRaw.get_exposures()
		DBHelperRaw.get_exposure_outcome()
		DBHelperRaw.get_population_subsets(1)
		DBHelperRaw.get_measurements()
		DBHelperRaw.get_outcomes()
		DBHelperRaw.get_mortalities()
		DBHelperRaw.get_samples() # for population and relative risks
		DBHelperRaw.get_risks()
		DBHelperRaw.get_bmi_measurements()

	@staticmethod
	def get_samples():
		"""This function returns all samples for outcomes of all exposures 

    		:param : 
   	 	:returns: No return 
    		"""
		DBHelperRaw.exposure_bins_rr = {}
		DBHelperRaw.exposure_bins = {}
		# all exposures
		for e_id in DBHelperRaw.exposures:
			#exposure id
			rr_bins		= []
			pop_bins	= []
			# related outcome risks

			with DBHelperRaw.con:
				cur_r = DBHelperRaw.con.cursor()
				cur_r.execute("SELECT bin_value FROM primemodel_exposurebins where exposure_id = %s and bin_type='r'",e_id)
				cur_p = DBHelperRaw.con.cursor()
				cur_p.execute("SELECT bin_value FROM primemodel_exposurebins where exposure_id = %s and bin_type='p'",e_id)

				while True:
					row_r = cur_r.fetchone()
					row_p = cur_p.fetchone()
					if row_r == None:
						break
					else:
						rr_bins.append(float(row_r[0]))
						pop_bins.append(float(row_p[0]))
				DBHelperRaw.exposure_bins_rr[e_id] 	= rr_bins
				DBHelperRaw.exposure_bins[e_id] 	= pop_bins



	@staticmethod
	def get_risks():
		"""This function returns all baseline risks for all exposures 

    		:param : 
   	 	:returns: No return 
    		"""
		DBHelperRaw.risks = {}
		
		#get risks from database table primemodel_relativerisks
		# all exposures
		for e_id in DBHelperRaw.exposures:#exposure id
			# related outcome ids
			e_o = DBHelperRaw.exposure_outcome
			outcome_ids = DBHelperRaw.exposure_outcome.get(e_id)
			# related outcome risks
			risks_outcomes= {}
			for o_id in outcome_ids:
				# get data from database
				o_risks = [] # risks for current outcome
				# add into risks list of current exposure
				with DBHelperRaw.con:
					cur = DBHelperRaw.con.cursor()
					cur.execute("SELECT risk_value FROM primemodel_relativerisk where exposure_id = %s and outcome_id=%s order by population_subset_id, id",(e_id,o_id))
					while True:
						row = cur.fetchone()
						if row == None:
							break
						else:
							o_risks.append(float(row[0]))	
				risks_outcomes[o_id] = o_risks
				# add into risks lists of all exposures
			DBHelperRaw.risks[e_id] = risks_outcomes

	
	@staticmethod
	def get_population_subsets(pop_id):
		"""This function retrieves population subsets from database, exposures store in a datastructure of [] 

    		:param pop_id: population id 
   	 	:returns: female age groups 
    		"""
		DBHelperRaw.population_total_size 	= 0	
		population_subsets 		= [] 
		with DBHelperRaw.con:
			cur = DBHelperRaw.con.cursor()
			cur.execute("SELECT age_group,gender,size FROM primemodel_populationsubset where population_id = %s order by id",pop_id)
			while True:
				row = cur.fetchone()
				if row == None:
					break
				else:
					# add into risks list of current exposure
					age_group 	= row[0] 
					gender 		= row[1] 
					size 		= int(row[2]) 
					DBHelperRaw.population_total_size  += size
					population_subsets.append({'age_group':age_group,'gender':gender,'size':size})
		DBHelperRaw.population_subsets	= population_subsets
		DBHelperRaw.age_group_num		= len(DBHelperRaw.population_subsets)

	@staticmethod
	def get_age_group(age_group_id):
		"""This function return age group according to age group id 

    		:param : 
   	 	:returns: No return 
    		"""
		age_group = DBHelperRaw.population_subsets[age_group_id].get('age_group')
		return age_group

	@staticmethod
	def get_measurements():
		"""This function retrieves all measurements from database, exposures store in a datastructure of {[]} 

    		:param : 
   	 	:returns: No return 
    		"""
		DBHelperRaw.measurements = {}
		for exposure_id in DBHelperRaw.exposures:
			DBHelperRaw.measurements[exposure_id] = DBHelperRaw.get_measurements_lists(exposure_id)#[[b_means],[c_means],[b_sds],[c_sds],[b_non_rates],[c_non_rates]]
			
	@staticmethod
	def get_bmi_measurements():
		"""This function retrieves all measurements bmi 

    		:param : 
   	 	:returns: No return 
    		"""
		DBHelperRaw.b_bmi_mean = DBHelperRaw.get_bmi_mean()
		DBHelperRaw.b_bmi_sd = DBHelperRaw.get_bmi_sd() 
		DBHelperRaw.b_energy_mean = DBHelperRaw.get_bmi_energy_total() 
		DBHelperRaw.b_height_mean = DBHelperRaw.get_bmi_height() 
		DBHelperRaw.b_sedentary_rate = DBHelperRaw.get_sedentary_rate() 
		DBHelperRaw.b_met_mean = DBHelperRaw.get_met_mean()
		DBHelperRaw.b_met_mvpa = DBHelperRaw.get_met_mvpa()
		DBHelperRaw.b_met_non_mvpa = DBHelperRaw.get_met_non_mvpa()
		
	@staticmethod
	def get_measurements_lists(exposure_id):
		"""This function retrieve all measurements for one exposure 

    		:param m_type_ids: measurement type id 
    		:type m_type_ids: list 
   	 	:returns: measurement list for one exposure 
    		"""
		lists = [] #list of one exposure mean/sd/non-rates, [baseline mean, counterfactual mean, baseline sd, counterfactual sd, baseline non rate, counterfactual non rate], for fats, it could be [baseline total fat mean, counterfactual total fat mean, baseline saturate fat mean, counterfactual saturate fat mean, ...]

		mean_ids 	= DBHelperRaw.get_measurement_type_id(exposure_id, 'Mean')
		sd_ids 		= DBHelperRaw.get_measurement_type_id(exposure_id, 'SD')
		percentage_ids 	= DBHelperRaw.get_measurement_type_id(exposure_id, 'Percentage') #could be empty list
		measuretype_ids = mean_ids + sd_ids + percentage_ids

		for measuretype_id in measuretype_ids : #measuretype_ids is in the format of [{'id':1},{'id':2}]
			if measuretype_id != None:
				lists.append(DBHelperRaw.get_measurements_list(measuretype_id,True)) #baseline measurements
				lists.append(DBHelperRaw.get_measurements_list(measuretype_id,False)) #counterfactual measurements

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

				b_mean_one_value= logic.get_balanced_mean(b_fat_means) # decimal value
				c_mean_one_value= logic.get_balanced_mean(c_fat_means) # decimal value
				b_sd_one_value	= logic.get_balanced_sd(b_fat_sds) # decimal value
				c_sd_one_value	= logic.get_balanced_sd(c_fat_sds) # decimal value

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
		with DBHelperRaw.con:
			cur = DBHelperRaw.con.cursor()
			if is_baseline:
				cur.execute("SELECT value FROM primemodel_measurement where measurement_type_id=%s and measurement_option='B' order by population_subset_id",m_type_id)
			else:
				cur.execute("SELECT value FROM primemodel_measurement where measurement_type_id=%s and measurement_option='C' order by population_subset_id",m_type_id)
			while True:
				row = cur.fetchone()
				if row == None:
					break
				else:
					values.append(float(row[0]))
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
		ids_num = []
		with DBHelperRaw.con:
			cur = DBHelperRaw.con.cursor()
			cur.execute("SELECT id FROM primemodel_measurementtype where exposure_id=%s and statistical_measure=%s order by id",(e_id,statistical_measure_type))
			while True:
				row = cur.fetchone()
				if row == None:
					break
				else:
					ids_num.append(int(row[0]))
		return ids_num


	@staticmethod
	def get_mortalities():
		"""This function retrieves all mortalities from database, exposures store in a datastructure of {} 

    		:param : 
   	 	:returns: No return 
    		"""
		DBHelperRaw.mortalities 	= {} # {outcome_id: outcome} 
		DBHelperRaw.total_mortality	= 0
		keys 				= DBHelperRaw.outcomes.keys()

		# outcome mortality
		for i in DBHelperRaw.outcomes.keys():
			mortality_nums 		= [] # mortality for one outcome
			with DBHelperRaw.con:
				cur = DBHelperRaw.con.cursor()
				cur.execute("SELECT value FROM primemodel_mortality where outcome_id=%s order by population_subset_id",i)
				while True:
					row = cur.fetchone()
					if row == None:
						break
					else:
						m_value = int(row[0])
						mortality_nums.append(m_value) 
			sum_mortality_outcome 		= sum(mortality_nums)
			DBHelperRaw.outcome_mortality[i]= sum_mortality_outcome # add into outcome mortality sum list	
			DBHelperRaw.total_mortality 	= DBHelperRaw.total_mortality + sum_mortality_outcome # add up to total baseline mortality 
			DBHelperRaw.mortalities[i]  	= mortality_nums 

		age_group_separator 	= DBHelperRaw.age_group_num/2 + 1 
		sum_mortality_male 	= 0# add into gender mortality sum list	
		sum_mortality_female 	= 0# add into gender mortality sum list	
		# age and gender mortality
		for i in xrange(1,DBHelperRaw.age_group_num + 1):
			with DBHelperRaw.con:
				cur = DBHelperRaw.con.cursor()
				cur.execute("SELECT sum(value) FROM primemodel_mortality where population_subset_id=%s order by outcome_id",i)
				while True:
					row = cur.fetchone()
					if row == None:
						break
					else:
						sum_mortality_age = int(row[0]) 
						if i < age_group_separator: # male
							sum_mortality_male 	= sum_mortality_male + sum_mortality_age # add up to gender mortality sum 
						else: # female
							sum_mortality_female 	= sum_mortality_female + sum_mortality_age # add up to gender mortality sum 
						DBHelperRaw.age_mortality[i] 	= sum_mortality_age # add into age mortality sum list	

		DBHelperRaw.gender_mortality['male'] 		= sum_mortality_male # add into gender mortality sum list	
		DBHelperRaw.gender_mortality['female']		= sum_mortality_female # add into gender mortality sum list	


	@staticmethod
	def get_exposures():
		"""This function retrieves all exposures from database, exposures store in a datastructure of [{}] 

    		:param : 
   	 	:returns: all exposures in database 
    		"""
		DBHelperRaw.exposures = {} 
		with DBHelperRaw.con:
			cur = DBHelperRaw.con.cursor()
                	cur.execute("SELECT id,name,dist_type FROM primemodel_exposure order by id")

			while True:
				row = cur.fetchone()
				if row == None:
					break
				else: 
					e_id 		= int(row[0])
					name		= row[1]
					dist_type	= int(row[2])
					DBHelperRaw.exposures[e_id] = {'name':name,'dist_type':dist_type} # all data fetched from database are in form of unicode 
					
	@staticmethod
	def get_outcomes():
		"""This function retrieves all outcomes from database, outcome store in a datastructure of {o_id:[name,abbreviation]} 

    		:param : 
   	 	:returns: No return 
    		"""
		DBHelperRaw.outcomes = {} 
		with DBHelperRaw.con:
			cur = DBHelperRaw.con.cursor()
                	cur.execute("SELECT id,name,abbreviation FROM primemodel_outcome order by id")

			while True:
				row = cur.fetchone()
				if row == None:
					break
				else:
					o_id 		= int(row[0])
					name		= row[1]
					abbreviation	= row[2]
					DBHelperRaw.outcomes[o_id] = [name,abbreviation] 
					

	@staticmethod
	def get_exposure_id(e_id):
		"""This function return exposure id according to exposure id 

    		:param abbreviation: outcome abbreviation 
    		:type abbreviation: string 
   	 	:returns: outcome id 
    		"""
		exposure_id = DBHelperRaw.exposures[e_id-1].get('id')
		return exposure_id

	@staticmethod
	def get_exposure_id_from_name(exposure_name):
		"""This function return exposure id according to exposure name 

    		:param exposure_name: exposure name 
    		:type exposure_name: string 
   	 	:returns: exposure id 
    		"""
		for eid in DBHelperRaw.exposures:
			if exposure_name == DBHelperRaw.exposures[eid].get('name'):
				return eid
		return None 

	@staticmethod
	def get_exposure_outcome():
		"""This function stores outcomes into database, exposure_outcome={exposure_id:}

    		:param : 
   	 	:returns: No return 
    		"""
		DBHelperRaw.exposure_outcome = {} 
		# fetch data from database
		with DBHelperRaw.con:
			cur = DBHelperRaw.con.cursor()
                	cur.execute("SELECT exposure_id,outcome_id,lower_limit_estimate,upper_limit_estimate,measure FROM primemodel_exposureoutcome order by id")

			# store data into an easy-to-search data format 
			outcome_ids 	= {} 
			e_id 		= 1
			while True:
				row = cur.fetchone()
				if row == None:
					break
				else:
					new_e_id= int(row[0])
					o_id 	= int(row[1])
					lle 	= float(row[2])
					ule 	= float(row[3])
					measure = float(row[4])
					if new_e_id == e_id: #the same exposure
						outcome_ids[o_id] 		= {'lower_limit_estimate':lle,'upper_limit_estimate':ule,'measure':measure}#store in a dictionary
					else: #a new exposure
						DBHelperRaw.exposure_outcome[e_id]	= outcome_ids; 
						outcome_ids 			= {} 
						outcome_ids[o_id] 		= {'lower_limit_estimate':lle,'upper_limit_estimate':ule,'measure':measure}#store in a dictionary
						e_id 				= new_e_id
			DBHelperRaw.exposure_outcome[e_id] = outcome_ids #{e_id:{o_id:[lle,ule]}} 

	@staticmethod
	def get_compound_exposure_outcome_ids(e_ids):
		"""This function return all relavant outcome ids for all exposures in e_ids

    		:param e_id: random exposure ids composure 
    		:type e_ids: list 
   	 	:returns: all relavant outcome ids for all exposures in e_ids 
    		"""
		outcome_ids = {}
		for e_id in e_ids:
			e_outcome_ids = DBHelperRaw.exposure_outcome[e_id] # all outcome_ids for one exposure,  {'lower_limit_estimate':lle,'upper_limit_estimate':ule,'measure':measure}#
			
	@staticmethod
	def get_outcome_name(o_id):
		"""This function return outcome name according to outcome id 

    		:param o_id: outcome id 
    		:type o_id: int 
   	 	:returns: outcome name 
    		"""
		return DBHelperRaw.outcomes.get(o_id)[0]

	@staticmethod
	def get_outcome_abbreviation(o_id):
		"""This function return outcome abbreviation according to outcome id 

    		:param o_id: outcome id 
    		:type o_id: int 
   	 	:returns: outcome abbreviation 
    		"""
		return DBHelperRaw.outcomes.get(o_id)[1]

	@staticmethod
	def get_outcome_id(abbreviation):
		"""This function return outcome id according to outcome abbreviation 

    		:param abbreviation: outcome abbreviation 
    		:type abbreviation: string 
   	 	:returns: outcome id 
    		"""
		o_id = 1
		for key in DBHelperRaw.outcomes.keys():
			if abbreviation == DBHelperRaw.outcomes.get(key)[1]:
				return key	
		return o_id

	@staticmethod
	def get_bmi_energy_total():
		"""This function get baseline energy total for bmi 

   	 	:returns: energy_total
    		"""
		with DBHelperRaw.con:
			cur = DBHelperRaw.con.cursor()
			cur.execute("SELECT value FROM primemodel_measurement where measurement_type_id=1 and measurement_option='B' order by population_subset_id")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				else:
					energy_total = float(row[0])#all energies value are same
					break
		return energy_total

	@staticmethod
	def get_bmi_height():
		"""This function get baseline energy total for bmi 

   	 	:returns: energy_total
    		"""
		height = 0 
		with DBHelperRaw.con:
			cur = DBHelperRaw.con.cursor()
			cur.execute("SELECT value FROM primemodel_measurement where measurement_type_id=27 and measurement_option='B' order by population_subset_id")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				else:
					height= float(row[0])#all energies value are same
					break
		return height 

	@staticmethod
	def get_bmi_mean():
		"""This function get baseline energy total for bmi 

   	 	:returns: energy_total
    		"""
		mean = 0 
		with DBHelperRaw.con:
			cur = DBHelperRaw.con.cursor()
			cur.execute("SELECT value FROM primemodel_measurement where measurement_type_id=28 and measurement_option='B' order by population_subset_id")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				else:
					mean = float(row[0])#
					break
		return mean 

	@staticmethod
	def get_bmi_sd():
		"""This function get baseline energy total for bmi 

   	 	:returns: energy_total
    		"""
		sd = 0 
		with DBHelperRaw.con:
			cur = DBHelperRaw.con.cursor()
			cur.execute("SELECT value FROM primemodel_measurement where measurement_type_id=29 and measurement_option='B' order by population_subset_id")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				else:
					sd = float(row[0])#
					break
		return sd 

	@staticmethod
	def get_met_mean():
		"""This function get baseline energy total for bmi 

   	 	:returns: energy_total
    		"""
		met_mean = 0 
		with DBHelperRaw.con:
			cur = DBHelperRaw.con.cursor()
			cur.execute("SELECT value FROM primemodel_measurement where measurement_type_id=22 and measurement_option='B' order by population_subset_id")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				else:
					met_mean= float(row[0])#
					break
		return met_mean 

	@staticmethod
	def get_sedentary_rate():
		"""This function get baseline energy total for bmi 

   	 	:returns: energy_total
    		"""
		rate= 0 
		with DBHelperRaw.con:
			cur = DBHelperRaw.con.cursor()
			cur.execute("SELECT value FROM primemodel_measurement where measurement_type_id=24 and measurement_option='B' order by population_subset_id")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				else:
					rate= float(row[0])#
					break
		return rate 

	@staticmethod
	def get_met_non_mvpa():
		"""This function get baseline energy total for bmi 

   	 	:returns: energy_total
    		"""
		non_mvpa = 0 
		with DBHelperRaw.con:
			cur = DBHelperRaw.con.cursor()
			cur.execute("SELECT value FROM primemodel_measurement where measurement_type_id=25 and measurement_option='B' order by population_subset_id")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				else:
					non_mvpa = float(row[0])#
					break
		return non_mvpa

	@staticmethod
	def get_met_mvpa():
		"""This function get baseline energy total for bmi 

   	 	:returns: energy_total
    		"""
		mvpa = 0 
		with DBHelperRaw.con:
			cur = DBHelperRaw.con.cursor()
			cur.execute("SELECT value FROM primemodel_measurement where measurement_type_id=26 and measurement_option='B' order by population_subset_id")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				else:
					mvpa = float(row[0])#
					break
		return mvpa 


	@staticmethod
	def get_test_data_bunch():
		"""This function fetches all test data from database 

   	 	:returns: test data 
    		"""
		DBHelperRaw.test_exposure_sequences = [] #[[{}]] 
		DBHelperRaw.test_results = [] #[1,2,...] 
		with DBHelperRaw.con:
			cur = DBHelperRaw.con.cursor()
			cur.execute("SELECT					total_energy_mean, \
                                                                                fruit_mean,\
                                                                                fruit_sd,\
                                                                                fruit_non_rate,\
                                                                                veg_mean,\
                                                                                veg_sd,\
                                                                                veg_non_rate,\
                                                                                fibre_mean,\
                                                                                fibre_sd,\
                                                                                salt_mean,\
                                                                                salt_sd,\
                                                                                total_fat_mean,\
                                                                                total_fat_sd,\
                                                                                saturate_fat_mean,\
                                                                                saturate_fat_sd,\
                                                                                mufa_fat_mean,\
                                                                                mufa_fat_sd,\
                                                                                pufa_fat_mean,\
                                                                                pufa_fat_sd,\
                                                                                dietary_cholesterol_mean,\
                                                                                dietary_cholesterol_sd,\
                                                                                met_mean,\
                                                                                met_sd,\
                                                                                sedentary_rate,\
                                                                                met_non_mvpa,\
                                                                                met_mvpa,\
                                                                                alcohol_low,\
                                                                                alcohol_mean,\
                                                                                alcohol_sd,\
                                                                                smoker_never,\
                                                                                smoker_previous,\
                                                                                smoker_current,\
                                                                                result FROM primemodel_testparameter")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				else:
					total_energy_mean 	= float(row[0]) #test_parameter.total_energy_mean
					fruit_mean 		= float(row[1]) #test_parameter.fruit_mean
					fruit_sd		= float(row[2]) #test_parameter.fruit_sd
					fruit_non_rate		= float(row[3]) #test_parameter.fruit_non_rate
					veg_mean		= float(row[4]) #test_parameter.veg_mean
					veg_sd			= float(row[5]) #test_parameter.veg_sd
					veg_non_rate		= float(row[6]) #test_parameter.veg_non_rate
					fibre_mean		= float(row[7]) #test_parameter.fibre_mean
					fibre_sd		= float(row[8]) #test_parameter.fibre_sd
					salt_mean		= float(row[9]) #test_parameter.salt_mean
					salt_sd			= float(row[10]) #test_parameter.salt_sd
					total_fat_mean		= float(row[11]) #test_parameter.total_fat_mean
					total_fat_sd		= float(row[12]) #test_parameter.total_fat_sd
					saturate_fat_mean	= float(row[13]) #test_parameter.saturate_fat_mean
					saturate_fat_sd		= float(row[14]) #test_parameter.saturate_fat_sd
					mufa_fat_mean		= float(row[15]) #test_parameter.mufa_fat_mean
					mufa_fat_sd		= float(row[16]) #test_parameter.mufa_fat_sd
					pufa_fat_mean		= float(row[17]) #test_parameter.pufa_fat_mean
					pufa_fat_sd		= float(row[18]) #test_parameter.pufa_fat_sd
					dietary_cholesterol_mean= float(row[19]) #test_parameter.dietary_cholesterol_mean
					dietary_cholesterol_sd	= float(row[20]) #test_parameter.dietary_cholesterol_sd
					met_mean		= float(row[21]) #test_parameter.met_mean
					met_sd			= float(row[22]) #test_parameter.met_sd
					sedentary_rate		= float(row[23]) #test_parameter.sedentary_rate
					met_non_mvpa		= float(row[24]) #test_parameter.met_non_mvpa
					met_mvpa		= float(row[25]) #test_parameter.met_mvpa
					alcohol_low		= float(row[26]) #test_parameter.alcohol_low
					alcohol_mean		= float(row[27]) #test_parameter.alcohol_mean
					alcohol_sd		= float(row[28]) #test_parameter.alcohol_sd
					smoker_never		= float(row[29]) #test_parameter.smoker_never
					smoker_previous		= float(row[30]) #test_parameter.smoker_previous
					smoker_current		= float(row[31]) #test_parameter.smoker_current
					result			= float(row[32]) #test_parameter.result
			
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
					DBHelperRaw.test_exposure_sequences.append(exposure_sequence)#a new exposure sequence
					DBHelperRaw.test_results.append(result)#all results in tests

