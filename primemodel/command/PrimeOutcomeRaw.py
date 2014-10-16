"""An Outcome Class. This class contains information about an outcome of an exposure, including information like relative risk, death rates, mortality, bins/samples, original baseline and final counterfactual mortality, it also provides death averted to present.
.. module:: PrimeOutcomeRaw
   :platform: Ubuntu Unix
   :synopsis: This class composes an Outcome object belonging to an Exposure object. 

.. moduleauthor:: Lijuan Marissa Zhou <marissa.zhou.cn@gmail.com>

"""
from DBHelperRaw import * 
from logic import * 

class PrimeOutcomeRaw:
	
	def __init__(self, name, outcome_id, exposure_id, mortality, samples, risks, lower_limit_estimate, upper_limit_estimate, measure):
		"""This function initialize an instance of current class Outcome 

    		:param name: outcome name like 'Stroke' or 'Lung Cancer', etc. 
    		:type name: string 
    		:param o_id: outcome id, same number as in the database 
    		:type o_id: int 
    		:param mortality: origianl mortality for current outcome, in 'Only' occasions, it is the original baseline mortality, in 'Compound' cases, it is counterfactual mortality of the same outcome of previous exposure 
    		:type mortality: list 
    		:param samples: samples/bins for relative risks 
    		:type samples: list 
    		:param lower_limit_estimate: relative risks estimate for lower bound 
    		:type lower_limit_estimate: list 
    		:param upper_limit_estimate: relative risks estimate for upper bound 
    		:type upper_limit_estimate: list 
    		:param measure: measure for the current outcome, it is the consumption measure like 7g/day or 20mm/week, for one outcome in one exposure, all population subsets have the same measure 
    		:type measure: float 
    		:param exposure_id: exposure id, this id is the same number as shown in the database 
    		:type exposure_id: int 
   	 	:returns: 
    		"""
		self.name 			= name # name of current outcome, this is kept with each outcome to present on the final interface
		self.outcome_id 		= outcome_id # outcome id: 1-24 in the DBHelper, or in the database 
		self.exposure_id 		= exposure_id
		self.mortality 			= mortality # inital mortality, the left side of outcome tables in excel
		self.samples 			= samples # [] samples for relative risks  
		self.risks 			= risks # {} initial risks, refer to papers 
		self.age_group_num 		= len(self.mortality) # row number of matrix
		self.measure_num 		= len(self.samples) # column number of matrix
		self.measure 			= measure # measure like 10g/day 
		self.lower_limit_estimate 	= lower_limit_estimate
		self.upper_limit_estimate 	= upper_limit_estimate
		
		self.relative_risks 		= [] # [][] 
		self.death_rates		= [] # [][] 
		self.b_deaths 			= [] # [][] deaths matrix for baseline 
		self.c_deaths 			= [] # [][] deaths matrix for counterfactual
		self.c_mortality 		= [] # [] mortality for counterfactual, this is used for next exposure in compound exposures, same format as self.mortality 
		self.b_mortality_sum 		= sum(self.mortality) 
		self.c_mortality_sum 		= self.b_mortality_sum

		self.deaths_changes 		= None # a list of death changes for different age groups, mortality-c_mortality 
		self.deaths_changes_sum 	= 0 # death sum for current outcome	 


	#################################################
	# realative risks				# 
	#################################################
	def get_relative_risk(self):
		"""This function return the relative risk for subsets, it does not need to know what data set is, this can not be started until a population input is fulfilled 

    		:param self: self attributes 
   	 	:returns: No return  
    		"""
		m 		= self.age_group_num # row number of matrix
		n 		= self.measure_num # column number of matrix
		sep_row 	= m / 2 # seperating point for row
		sep_col 	= n # seperating point for column 
		
		# breast cancer in bmi is different from others as male relative risks are set to be 1.0 only and inital female relative risks differ as age change
		if self.exposure_id == 7 and ( self.outcome_id == 9 or self.outcome_id == 2): # 9 is breast cancer and 2 is CHD
			relative_risks = [[0 for x in range(n)] for x in range(m)] # initial the relative risk matrix with all 0 value
			e_id			= self.exposure_id # exposure id 
			o_id			= self.outcome_id # outcome id 
			self.relative_risks 	= self.single_sex_relative_risk(m,n) # relative risks when gender affects 
		else:
			relative_risks = [[0 for x in range(n)] for x in range(m)] # initial the relative risk matrix with all 0 value
			for i in xrange(m):		
				lower_limit 	= 0 
				for j in xrange(n):
					# the first relative risk is always 1.0
					if j == 0: 
						relative_risks[i][0] = 1.0 
						continue
					# all bins neither the first bin nor the last bin
					if j < n-1: 
						sample_distance = self.samples[j+1] - self.samples[j] # sample distance might be changing
					upper_limit_reestimate  = float(self.upper_limit_estimate) + sample_distance / 2 # re estimate limit,can be changed 
					if self.samples[j] <= self.lower_limit_estimate: # lower than the estimate according to referrence
						relative_risks[i][j] 	= 1.0 
						lower_limit 		= j 
					elif self.samples[j] > self.upper_limit_estimate: # higher than the estimate according to referrence
						relative_risks[i][j] = relative_risks[i][j-1]
					else:
						# parameter expousure id is DBHelper id, same as in the database
						# for different exposures there are different relative risk calculation methods
						if self.exposure_id in (1, 2, 3): # fruit or veg or fiber, risks decrease in linear relationship
							relative_risks[i][j] 	= self.linear_relative_risk_decrease(i,j,lower_limit) 
						elif self.exposure_id in (4, 5): # salt or fat, risks increase in linear relationship
							relative_risks[i][j] 	= self.linear_relative_risk_increase(i,j,lower_limit) 
						elif self.exposure_id == 6: # phisical activity
							# need to add inactive rate from b/c table
							relative_risks[i][j] 	= self.pa_relative_risk(i,j) 
						elif self.exposure_id == 7: # bmi,sample amount 
							relative_risks[i][j] 	= self.categorical_relative_risk(i,j,self.risks[j],relative_risks[i][j-1])
						elif self.exposure_id == 8: # alcohol
							if self.outcome_id == 9: # breast cancer in alchohol 
								if i< sep_row:
									relative_risks[i][j] 	= 1.0 
								else:
									relative_risks[i][j] 	= self.linear_relative_risk_decrease(i,j,lower_limit) 
							# for some outcomes, risks decrease in linear relationship
							if self.outcome_id in (3, 8, 16): 
								relative_risks[i][j] 	= self.linear_relative_risk_decrease(i,j,lower_limit) 
							# for some outcomes, relative risks have fixed rates
							elif self.outcome_id in (1, 2, 14, 19): 
								if i > sep_row:
									relative_risks[i][j] 	= self.risks[j+sep_col] 
								else:
									relative_risks[i][j] 	= self.risks[j] 
							else:
								pass
						elif self.exposure_id == 9: # smoking 
							# Relative risks are fixed. 
							# Convert one dimensional array of these static risks from database into a two dimensional matrix, applying that static value to each bin in the esposure/population distribution  
							relative_risks[i][j] 	= self.risks[i*3+j]
						else:
							pass
			self.relative_risks = relative_risks

		
	def single_sex_relative_risk(self, m, n):
		"""This function calculate relative risk value for categorical distribution like physical activity 

    		:param m: row number 
    		:type m: int 
    		:param n: column number 
    		:type n: int 
   	 	:returns: current relative risk value 
    		"""
		relative_risks = [[0 for x in range(n)] for x in range(m)] # initial the relative risk matrix with all 0 value
		# male relative risks
		for i in xrange(m/2):		
			relative_risks[i][0] = 1.0 
			# breast cancer, for male relative risk, it is always 1.0
			if self.outcome_id == 9:
				for j in xrange(1,n):
					relative_risks[i][j] = 1.0 
			# CHD, male and female are using different parameters 
			elif self.outcome_id == 2:
				for j in xrange(1,n):
					initial_risk 		= self.risks[j]
					relative_risks[i][j] 	= self.categorical_relative_risk(i,j, initial_risk, relative_risks[i][j-1])
		# female relative risks
		for i in xrange(m/2, m):		
			relative_risks[i][0] = 1.0 
			# breast cancer
			if self.outcome_id == 9:
				for j in xrange(1,n):
					# Pre-menopausal 
					if i < AGE_SEPERATOR_BREAST_CANCER:
						initial_risk 	= self.risks[j]
					# Post-menopausal
					else: 
						initial_risk 	= self.risks[j+n]
					relative_risks[i][j] 	= self.categorical_relative_risk(i,j, initial_risk, relative_risks[i][j-1])
			# CHD 
			elif self.outcome_id == 2:
				for j in xrange(1,n):
					initial_risk 		= self.risks[j+n]
					relative_risks[i][j] 	= self.categorical_relative_risk(i,j, initial_risk, relative_risks[i][j-1])
		return relative_risks
	
					
	def pa_relative_risk(self, i, j):
		"""This function calculates relative risk value for physical activity 

    		:param i: row number 
    		:type i: int 
    		:param j: column number 
    		:type j: int 
   	 	:returns: current relative risk value 
    		"""
		frac1 			= self.risks[i] - 1.0
		frac2 			= get_pow(self.samples[j],0.25)
		frac3 			= get_pow(self.measure,0.25)
		rr 			= 1 + (( frac1 / frac3 ) * frac2 )
		return rr

	def categorical_relative_risk(self, i, j, initital_risk, previous_risk):
		"""This function calculates relative risk value for categorical distribution like alcohol/BMI

    		:param i: row number 
    		:type i: int 
    		:param j: column number 
    		:type j: int 
   	 	:returns: current relative risk value 
    		"""
		measure_difference	= self.samples[j] - self.samples[j-1] 
		frac2 			= measure_difference / (self.measure + 0.0)
		risk_factor		= get_pow(initital_risk,frac2)
		relative_risk 		= risk_factor * previous_risk
		return relative_risk 

	def linear_relative_risk_decrease(self, i, j, lower_limit):
		"""This function calculates relative risk value for linear distribution in a decrease case, in which relative risk decreases as consumption decreases 

    		:param i: row number 
    		:type i: int 
    		:param j: column number 
    		:type j: int 
    		:param lower_limit: lower limit of current exposure 
    		:type lower_limit: int 
   	 	:returns: current relative risk value 
    		"""
		risk 			= self.risks
		measure			= self.measure
		frac1 			= self.risks[i] #original risks from references stored in database
		measure_difference	= self.samples[j] - self.samples[lower_limit] 
		frac2 			= measure_difference / (self.measure + 0.0)
		rr 			= get_pow(frac1,frac2)
		return rr 

	def linear_relative_risk_increase(self, i, j, lower_limit):
		"""This function calculates relative risk value for linear distribution in an increase case, in which relative risk decreases as consumption increases  

    		:param i: row number 
    		:type i: int 
    		:param j: column number 
    		:type j: int 
    		:param lower_limit: lower limit of current exposure 
    		:type lower_limit: int 
   	 	:returns: current relative risk value 
    		"""
		frac1 			= 1.0 / self.risks[i]
		measure_difference	= self.samples[j] - self.samples[lower_limit] 
		frac2 			= measure_difference / (self.measure + 0.0)
		rr 			= get_pow(frac1,frac2)
		return rr 

	#################################################
	# death rates					#  
	#################################################
	def get_death_rates(self, population_distribution):
		"""This function starts the calculation of death rates for population subsets, it does not need to care what subset it is dealing with, the population distribution can be one line of population distribution for one subset or multiple lines of populaiton distribution for multiple subsets

    		:param mortality: original mortality 
    		:type mortality: list
    		:param population_distribution: this calculation needs population distribution, matrix or line if there is only one population subset  
    		:type population_distribution: list 
    		:param relative_risks: relative risks from last step 
    		:type relative_risks: list
   	 	:returns: 
    		"""
		# column and row for a matrix
		m = self.age_group_num
		n = self.measure_num
		# initiate the matrix
		death_rates = [[0 for x in range(n)] for x in range(m)] # initial the death rate matrix with all 0 value
		for i in xrange(m):
			this_mort 		= self.mortality[i]
			this_pop_dist 		= population_distribution[i]
			this_rr 		= self.relative_risks[i]
			# the first death rate needs to refer to the population distribution
			death_rates[i][0] 	= self.get_baseline_death_rate(this_mort,this_pop_dist,this_rr) # first death rate relies on population
			for j in xrange(1,n):
				# rest of the line is a multiple result of relative risk and the first column of death rate
				death_rates[i][j] = death_rates[i][0] * self.relative_risks[i][j] # the first column death rate multiply by current relative risk
		self.death_rates = death_rates

	def get_baseline_death_rate(self, base_mortality, population_distribution_line, relative_risks_line):
		"""This function returns the baseline death rate for death rates calculation,  in each row, all other rates are relying on this base rate 

    		:param base_mortality: base mortality, either from baseline data [only exposures] or from previous exposure result [compound] 
    		:type base_mortality: list 
    		:param population_distribution_line: the relavent line in population distribution 
    		:type population_distribution_line: list 
    		:param relative_risks_line: the relavent line in relative risk
    		:type relative_risks_line: list 
   	 	:returns: 
    		"""
		baseline_death_rate 	= 1000.0 * base_mortality 
		weighted_sum 		= 0.0
		for j in xrange(self.measure_num):
			this_pop_dist 	= population_distribution_line[j]
			this_rr 	= relative_risks_line[j] 
			weighted_sum 	+= this_rr * this_pop_dist 
		baseline_death_rate 	= baseline_death_rate / weighted_sum  
		return baseline_death_rate 


	#################################################
	# deaths					# 
	#################################################
	def get_deaths(self, b_population_distribution, c_population_distribution):
		"""This function starts calculating deaths for a subset data, without concering baseline or counterfactual, 

    		:param population_distribution: the relavent population distribution 
    		:type population_distribution: list 
    		:param death_rates: death rates 
    		:type death_rates: list 
   	 	:returns: No return 
    		"""
		m 		= self.age_group_num
		n 		= self.measure_num
		self.c_deaths 	= [[0 for x in range(n)] for x in range(m)] # initial the counterfactual death matrix with all 0 value
		self.b_deaths 	= [[0 for x in range(n)] for x in range(m)] # initial the baseline death matrix with all 0 value, b_deaths can be avoid when considering efficiency of the code, as it does not affect the counterfactual result in any way.
		for i in range(m):
			for j in range(n):
				# death is a multiple result of population and death rate
				self.b_deaths[i][j] = b_population_distribution[i][j] * self.death_rates[i][j] / 1000.0
				self.c_deaths[i][j] = c_population_distribution[i][j] * self.death_rates[i][j] / 1000.0


	def get_c_mortality(self):
		""" calculate counterfactual mortalities 

    		:param self: self attributes 
   	 	:returns: No return 
    		"""
		self.c_mortality = [] # final counterfactual mortality, each elements in the list is the death sum for a population subset
		for i in range(len(self.c_deaths)):
			# each value in c_mortality is sum of the line of deaths
			self.c_mortality.append(sum(self.c_deaths[i]))
		self.c_mortality_sum = sum(self.c_mortality) # total number of all counterfactual death of current expsoure and outcome pair

	
	#################################################
	# death changes					# 
	#################################################
	def get_deaths_changes_sum(self):
		""" return death changes sum 

    		:param self: self attributes 
   	 	:returns: death change sum 
    		"""
		self.deaths_changes_sum = get_deaths_sum(True) - get_deaths_sum(False)
		return self.deaths_changes_sum 


	def get_deaths_changes(self, b_deaths, c_deaths):
		""" Deaths sum change for both counterfactual compared with baseline subsets 

    		:param b_deaths: baseline deaths  
    		:type b_deaths: list 
    		:param c_deaths: counterfactual deaths
    		:type c_deaths: list 
   	 	:returns: death sum change 
    		"""
		m 			= self.age_group_num # length of population subsets
		self.deaths_changes 	= [0 for x in range(m)] # initiate the list with value 0
		for i in xrange(m):
			# get an array of death changes
			self.deaths_changes[i] = sum(c_deaths[i]) - sum(b_deaths[i])  
		return self.deaths_changes #[changes,changes...]


	def get_deaths_sum(self, is_baseline):
		""" Deaths sum returning function, baseline/counterfactual 

    		:param is_baseline: true is baseline, false is counterfactual 
    		:type is_baseline: bool 
   	 	:returns: death sum for baseline/counterfactual 
    		"""
		sum_deaths = 0
		if is_baseline:
				# sum of baseline deaths
				sum_deaths = sum(self.mortality) 
		else:
				# sum of counterfactual deaths
				sum_deaths = sum(self.c_mortality) 
		return sum_deaths

		
	#################################################
	# get and set attributions			# 
	#################################################
	def get_attr_lower_limit_estimate(self):
		"""This function return the class attribution lower limit estimate 

    		:param self: self attributes 
   	 	:returns: lower limit estimate 
    		"""
		return self.lower_limit_estimate


	def get_attr_upper_limit_estimate(self):
		"""This function return the class attribution upper limit estimate 

    		:param self: self attributes 
   	 	:returns: upper limit estimate 
    		"""
		return self.upper_limit_estimate


	def set_attr_mortalities(self, mortalities):
		"""This function set class attribution mortalities, it is necessary when calculating compound exposures, current baseline mortality should be counterfactual mortality of previous exposure 

    		:param mortalites: original mortalities 
   	 	:returns: No return 
    		"""
		self.mortalities = mortalities


	def get_attr_c_deaths(self):
		"""This function get class attribution deaths in counterfactual 

    		:param self: self attributes 
   	 	:returns: deaths matrix of the current outcome 
    		"""
		return self.c_deaths


	def get_attr_death_rates(self):
		"""This function return class attribution death rates 

    		:param self: self attributes 
   	 	:returns: death rates matrix of the current outcome 
    		"""
		return self.death_rates


	def get_attr_c_mortality(self):
		"""This function return the mortality for all age groups  

    		:param self: self attributes 
   	 	:returns: counterfactual mortality 
    		"""
		return self.c_mortality


	def get_attr_name(self):
		"""This function return the class attribution name of current outcome 

    		:param self: self attributes 
   	 	:returns: outcome name 
    		"""
		return self.name 


	def get_attr_id(self):
		"""This function return the class attribution id of current outcome 

    		:param self: self attributes 
   	 	:returns: outcome id 
    		"""
		return self.outcome_id
