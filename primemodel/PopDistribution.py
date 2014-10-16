"""An population distribution Class, this class initiate an matrix to store exposure distribution over bins according to distribution type, normal distribution or log normal distribution. It also includes some funtions that manipulate the distribution. Some of the functions are expandable for other usage. In the whole calculation procedure, there shouldn't be int or round to cut the precise of final result 
.. module:: ExposureDistribution 
   :platform: Ubuntu Unix
   :synopsis: A module for containing all population associations for Exposures 

.. moduleauthor:: Lijuan Marissa Zhou <marissa.zhou.cn@gmail.com>

"""
from primemodel.logic import * 
from primemodel.DBHelper import DBHelper 

class PopDistribution:
	def __init__(self, population_subsets, b_non_rate, b_mean, b_sd, c_non_rate, c_mean, c_sd, bins_pop, dist_type):
		""" intitiate an ExposureDistribution object 

    		:param population_subsets: age groups, in uk 2007 population case, it is 30 age group subsets 
    		:type population_subsets: list 
    		:param b_non_rate: non rate for non drinkers/non smokers etc. 
    		:type b_non_rate: list 
    		:param b_mean: baseline mean 
    		:type b_mean: list 
    		:param b_sd: baseline standard deviation 
    		:type b_sd: list 
    		:param c_non_rate: non rate for non drinkers/non smokers etc. In the excel model, some rates are based on 100, some are based on 1, in the database all rated are modified to be 100 based. 
    		:type c_non_rate: list 
    		:param c_mean: counterfactual mean 
    		:type c_mean: list 
    		:param c_sd: counterfactual standard deviation 
    		:type c_sd: list 
    		:param bins_pop: samples/bins for population 
    		:type bins_pop: list 
    		:param dist_type: distribution type, 0:normal or 1:lognormal, costant definition is in DBHelper class
    		:type dist_type: int 
    		:returns: no return 
    		"""
		self.age_group_num 	= len(population_subsets) # row number of matrix
		self.population_subsets	= population_subsets # [] list of population subsets
		self.b_non_rate		= b_non_rate 	# [] list of baseline non rates 
		self.b_mean 		= b_mean 	# [] list of basline means for different age groups 
		self.b_sd 		= b_sd 		# [] list of basline standard deviation for different age groups 
		self.c_non_rate		= c_non_rate 	# [] list of counterfactual non rates 
		self.c_mean 		= c_mean 	# [] list of counterfactual means for different age groups 
		self.c_sd 		= c_sd 		# [] list of counterfactual standard deviation for different age groups 

		'''
			log means and standard deviations
		'''
		b_log_mean_sds		= get_log_mean_sd(b_mean,b_sd) # returns [log_mean, log_sd]
		c_log_mean_sds		= get_log_mean_sd(c_mean,c_sd) # returns [log_mean, log_sd]
		self.b_log_mean		= b_log_mean_sds[0] # baseline log mean 
		self.b_log_sd		= b_log_mean_sds[1] # baseline log sd 
		self.c_log_mean 	= c_log_mean_sds[0] # counterfactual log mean 
		self.c_log_sd		= c_log_mean_sds[1] # counterfactual log sd 

		self.bins_pop		= bins_pop 	# [] bins for population distribution
		self.measure_num 	= len(bins_pop) # column number of matrix
		self.dist_type 		= dist_type 	# distribution type, normal/log

		'''
		 	final distributions	
		'''
		self.b_distribution 	= None # [][] baseline distribution 
		self.c_distribution 	= None # [][] counterfactual distribution 

	#################################################
	# start to get population distribution 		#
	#################################################
	def get_population_distributions(self, e_id): 
		""" This function gets exposure distribution for all both baseline and counterfactual exposures. e_id decides the distribution should be normal or lognormal or others 

    		:param e_id: exposure id 
    		:type e_id: int 
    		:returns: population distribution, it is a two dimensional list, [[population value]] where population value is the population size in each bin 
    		"""
		self.b_distribution = self.get_population_distribution(e_id,self.b_mean,self.b_sd,self.b_log_mean,self.b_log_sd,self.b_non_rate) # baseline population distribution
		self.c_distribution = self.get_population_distribution(e_id,self.c_mean,self.c_sd,self.c_log_mean,self.c_log_sd,self.c_non_rate) # counterfactual population distribution

	def get_population_distribution(self, e_id, mean, sd, log_mean, log_sd, non_rate):
		""" This function gets exposure distribution for all population subsets. e_id decides the distribution should be normal or lognormal or others 

    		:param e_id: exposure id 
    		:type e_id: int 
    		:param age_group: age_group 
    		:type age_group: list 
    		:param mean: mean 
    		:type mean: list 
    		:param sd: sd 
    		:type sd: list 
    		:param log_mean: log_mean 
    		:type log_mean: list 
    		:param log_sd: log_sd 
    		:type log_sd: list 
    		:param m: age group num 
    		:type m: int 
    		:param n: measure num 
    		:type n: int 
    		:returns: population distribution, it is a two dimensional list, [[population value]] where population value is the population size in each bin 
    		"""
		m 		 = self.age_group_num  # row number
		n 		 = self.measure_num 	# column number
		pop_distribution = [[0 for x in range(n)] for x in range(m)] # initialize the matrix with value 0
		# this is special for Smoking exposure, it is binary distribution, population is the multiply result
		if e_id == 9:
			for i in range(m):
				# population in current age group
				age_group_size 		= long(self.population_subsets[i].get('size')) # not int() or round() 
				pop_distribution[i][0] 	= age_group_size * non_rate[i] # non smoker rate 
				pop_distribution[i][1] 	= age_group_size * mean[i] # previous smoker 
				pop_distribution[i][2] 	= age_group_size * sd[i] # current smoker 
			return pop_distribution 

		# this is for all other exposures apart from Smoking 
		for i in range(m):
			# whole number of age group i, like how many people in age group 15-20
			age_group_size 			= long(self.population_subsets[i].get('size')) 
			if non_rate != None:
				population_non_rate	= age_group_size * non_rate[i]/100.0 # population non consumers	
				population_ex_non_rate	= age_group_size - population_non_rate # population excluding non consumers	
			else:
				population_ex_non_rate	= age_group_size 
			# this loop fills all population sizes in all bins
			for j in range(n):
				if j == n-1:#last one
					is_last 	= True
					# the desity of the last population bin is 1 minus previous one
					density		= get_population_density(population_ex_non_rate,upper,lower,mean[i],sd[i],log_mean[i],log_sd[i],self.dist_type,is_last)
				else:
					is_last 	= False 
					upper 		= self.bins_pop[j] 
					# need to specify lower boundary of bin 
					if j == 0:
						lower 	= 0 # the first bin 
					else:
						lower 	= self.bins_pop[j-1] 
					# the desity of the population bin is current bin density multiply by population size, log_mean log_sd might be rounded, different precision affects population numbers 
					dist_type 	= self.dist_type
					density		= get_population_density(population_ex_non_rate,upper,lower,mean[i],sd[i],log_mean[i],log_sd[i],self.dist_type, is_last)
					if j == 0 and non_rate != None:
						density+= population_non_rate # the first row number added up by non drinker/smoker etc.  
				pop_distribution[i][j] 	= density # assigned to pop_distribution matrix 
		return pop_distribution 


	#################################################
	# get and set attributions			#
	#################################################
	def get_attr_b_distribution(self):
		""" get attribution  baseline distribution of this class 

    		:param self: self attributes 
    		:returns: baseline population distribution 
    		"""
		return self.b_distribution

	def get_attr_c_distribution(self):
		""" get attribution counterfactual distribution of this class 

    		:param self: self attributes 
    		:returns: counterfactual population distribution 
    		"""
		return self.c_distribution

	def get_attr_b_log_mean(self):
		""" get attribution  baseline log mean of this class 

    		:param self: self attributes 
    		:returns: baseline log mean 
    		"""
		return self.b_log_mean

	def get_attr_b_log_sd(self):
		""" get attribution  baseline log standard deviation of this class 

    		:param self: self attributes 
    		:returns: baseline log standard deviation 
    		"""
		return self.b_log_sd

	def get_attr_bins_pop(self):
		""" get attribution samples for population distribution of this class 

    		:param self: self attributes 
    		:returns: samples for population distribution 
    		"""
		return self.bins_pop
