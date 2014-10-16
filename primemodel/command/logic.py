"""logic operation class
   This class includes all logic processing functions like get normal distribution, get average number etc.
.. module:: logic 
   :platform: Ubuntu Unix
   :synopsis: A module for all type of mathematical operation needed for Prime model

.. moduleauthor:: Lijuan Marissa Zhou <marissa.zhou.cn@gmail.com>

"""
from scipy.stats import norm,lognorm
import math
import scipy

'''
 	constants for distritubion types	
'''
DIST_TYPE_NORMAL 	= 0
DIST_TYPE_LOGNORMAL 	= 1 
DIST_TYPE_BINARY 	= 2 

INFINITE_GREAT 		= float("infinity") 
INFINITE_SMALL 		= float("-infinity") 

AGE_SEPERATOR_BREAST_CANCER = 24 #55-50 age and above, relative risks are changed 

'''
	parameters for different types of fats, these display correllation between different types of fats
'''
PARA_FAT		= [0.02,0.052,0.005,-0.026,0.0007] # a list of fats weights transmited into cholestrol. get from database


def get_norm_distribution(mean, sd):
	'''This :returns a normation distribution referring to given mean and standard deviation 
	
	:param mean: mean 
	:type mean: float 
	:param sd: standard deviation 
	:type sd:  float 
	:returns: normal distribution 
	'''
	distribution = norm(loc=mean,scale=sd)
	return distribution	

def get_population_density(size, upper, lower, mean, sd, log_mean, log_sd, dist_type, position_marker):
	'''This function returns a value of a population distribution, aka population size in a bin between lower and upper 
	
	:param size: total size 
	:type size: float 
	:param upper: upper value of bin 
	:type upper: float 
	:param lower: lower value of bin 
	:type lower: float 
	:param mean: mean 
	:type mean:  float 
	:param log_mean: log mean 
	:type log_mean: float 
	:param sd: standard deviation 
	:type sd: float 
	:param log_sd: log standard deviation 
	:type log_sd: float 
	:param dist_type: distribution type, normal, log or binary 
	:type dist_type: int 
	:param position_marker: is the last/first bin of samples or not, -1: first bin; 1: last bin; 0:any bin between the first and the last
	:type position_marker: int 
	:returns: population density 
	'''
	density = None
	if dist_type == DIST_TYPE_NORMAL:
		density = get_population_density_norm(size,upper,lower,mean,sd,position_marker)
	elif dist_type == DIST_TYPE_LOGNORMAL:
		density = get_population_density_lognorm(size,upper,lower,log_mean,log_sd,mean,sd,position_marker)
	else:
		density = get_population_density_norm(size,upper,lower,mean,sd,position_marker)
	return density

def get_population_density_norm(size, upper, lower, mean, sd, is_last):
	'''This :returns a value of a normal population distribution
	
	:param size: total size 
	:type size: float 
	:param upper: upper value of bin 
	:type upper:  float 
	:param lower: lower value of bin 
	:type lower:  float 
	:param mean: mean 
	:type mean:  float 
	:param sd: standard deviation 
	:type sd:  float 
	:param is_last: is the last bin of samples or not
	:type is_last: bool 
	:returns: population density 
	'''
	distribution = norm(loc=mean,scale=sd)
	if is_last: 
		cdf1 = 1
	else: 
		cdf1 = distribution.cdf(upper)
	if lower == 0:
		cdf2 = 0
	else:
		cdf2 = distribution.cdf(lower) 
	posibility_space = cdf1-cdf2 
	population = size * posibility_space 
	return population;

def get_population_density_lognorm(size, upper, lower, log_mean, log_sd, mean, sd, position_marker):
	'''This :returns a value of a lognormal population distribution
	
	:param size: total size 
	:type size: float 
	:param upper: upper value of bin 
	:type upper:  float 
	:param lower: lower value of bin 
	:type lower:  float 
	:param log_mean: log mean 
	:type log_mean:  float 
	:param log_sd: log standard deviation 
	:type log_sd:  float 
	:param mean: mean 
	:type mean:  float 
	:param sd: standard deviation 
	:type sd:  float 
	:param position_marker: is the last/first bin of samples or not, -1: first bin; 1: last bin; 0:any bin between the first and the last
	:type position_marker: int 
	:returns: population density 
	'''
	distribution 	= lognorm(loc=log_sd,scale=log_mean)
	if position_marker: 
		cdf1 	= 1
		lower 	= upper
	else: 
		cdf1 	= logncdf(upper,log_mean,log_sd)
	cdf2 		= logncdf(lower,log_mean,log_sd)
	posibility_space = cdf1 - cdf2 
	population 	= size * posibility_space 
	population_int 	= population
	return population_int;

# different from LN in excel by not adding +1
def get_log_mean_sd(means, sds):
	'''This returns log standard deviation of given mean and standard deviation lists
	
	:param means: mean list 
	:type means: list 
	:param sds: standard deviation list 
	:type means: list 
	:returns: log mean and standard deviation list 
	'''
	log_means 		= []
	log_sds 		= []
	for i in range(len(means)):
		mean 		= means[i]
		sd 		= sds[i]
		log_sd 		= math.sqrt(math.log1p(math.pow(sd,2)/math.pow(mean,2))) 
		log_mean 	= math.log1p(mean-1) - 0.5*log_sd*log_sd
		log_means.append(log_mean)
		log_sds.append(log_sd)
	return [log_means,log_sds] 

def get_pow(x, y):
	'''This returns x power of y 
	
	:param x: base 
	:type x: float 
	:param y: exponention 
	:type y: float 
	:returns: log mean and standard deviation list 
	'''
	return math.pow(x,y)

def get_sum_matrix(matrix):
	'''This returns sum of matrix  
	
	:param matrix: matrix to sum up 
	:type matrix: matrix 
	:returns: sum of matrix 
	'''
	if matrix == None:
		return 0
	sum_matrix = 0
	for row in matrix:
		sum_matrix += sum(row)
	return sum_matrix 

def logncdf(x,mean,sig):
	'''This returns log cdf value of a given distribution  
	
	:param x: x value of distribution 
	:type x: float 
	:param mean: mean value of distribution 
	:type mean: float 
	:param sig: sig value of distribution 
	:type sig: float 
	:returns: log cdf value 
	'''
	if x<0:
        	cdf  = 0.
    	elif scipy.isposinf(x):
		cdf  = 1.
	else: 
        	z    = (scipy.log(x)-mean)/float(sig)
        	cdf  = .5*(math.erfc(-z/scipy.sqrt(2)))
    	return cdf

def generate_list_value(v,n):
	'''This returns a size n list of same value  
	
	:param v: value of list 
	:type v: float 
	:param n: size of the list 
	:type n: float 
	:returns: a list of values 
	'''
	values = []
	for i in range(n):
		values.append(v)
	return values

def get_balanced_mean(mean_list):
	'''This returns a balanced mean for the mean_list with parameters for each mean stored in para_list 
	
	:param mean_list: mean value list for different statistical factors 
	:type mean_list: list 
	:param para_list: parameters list 
	:type para_list: list 
	:returns: a balanced mean value for means listed in mean_list 
	'''
 	#fat_means_paras = [0.02,0.052,0.005,-0.026,0.0007] # a list of fats weights transmited into cholestrol. get from database

	balanced_mean = 0 
	length = len(mean_list)
	for i in range(length):
		balanced_mean += mean_list[i]*PARA_FAT[i]
	return balanced_mean

def get_balanced_sd(sd_list):
	'''This returns a balanced sd for the sd_list with parameters for each mean stored in para_list 
	
	:param mean_list: mean value list 
	:type mean_list: list 
	:param para_list: parameters list 
	:type para_list: list 
	:returns: a balanced mean value for means listed in mean_list 
	'''
	length 			= len(sd_list)
	var_covariances 	= [[0 for x in range(length)] for x in range(length)] # half sparse matrix
	weight_covariances 	= [[0 for x in range(length)] for x in range(length)] # half sparse matrix

	# get variance and covariances for each 2 factors pair
	for i in range(length): #for fat it is 0,1,2,3,4
		var_covariances[i][i] = get_variance(sd_list[i]) #0.73 should be more variable 
		for j in range(0,i):
			var_1 = var_covariances[i][i]
			var_2 = var_covariances[j][j]
			var_covariances[i][j] = get_covariance(var_1,var_2,0.73) #0.73 should be more variable 

	# get weighted covariance
	for i in range(length): #for fat it is 0,1,2,3,4
		for j in range(0,i+1):
			weight_covariances[i][j] = var_covariances[i][j] * PARA_FAT[i] * PARA_FAT[j] 
		
	# sum up weighted covariances to and sqrt to get co related standard deviation of cholestrol
	co_sd 			= 0 # co related standard deviation 
	for i in range(length): #for fat it is 0,1,2,3,4
		for j in range(0,i+1):
			if i == j:
				co_sd += weight_covariances[i][j] # same fat
			else:
				co_sd += weight_covariances[i][j] * 2 # different fats
	co_sd = math.sqrt(co_sd)	
	return co_sd 

def get_variance(sd):
	'''This returns variance of one statistical factor 
	
	:param sd: standard deviation  
	:type sd: numeric 
	:returns: variance 
	'''
	return sd*sd 

def get_covariance(variance_1, variance_2, parameter):
	'''This returns covariance of two statistical factors 
	
	:param variance_1: variance for factor 1 
	:type variance_1: numeric 
	:param variance_2: variance for factor 2 
	:type variance_2: numeric 
	:returns: covariance of two statistical factors 
	'''
	fac1 = variance_1 * variance_2
	fac2 = math.sqrt(fac1)
	fac3 = parameter * fac2
	return fac3

def get_bmi_counterfactual_mean(b_bmi_mean, b_energy_mean, c_energy_mean, b_height_mean, b_sedentary_rate, b_met_mean, b_met_mvpa, b_met_non_mvpa, c_sedentary_rate, c_met_mean, c_met_mvpa, c_met_non_mvpa, ismale):
	'''This returns counterfactual mean for BMI, sd keeps the same as baseline sd 
	
	:param b_mean: baseline mean 
	:type b_mean: numeric 
	:param b_mean: baseline mean 
	:type b_mean: numeric 
	:returns: covariance of two statistical factors 
	'''
	para1 	= 0.0041868
	para2_m	= 17.7 
	para2_f	= 20.7 
	
	b_pal_mean = get_pal_mean(b_sedentary_rate, b_met_mean, b_met_mvpa, b_met_non_mvpa) 
	c_pal_mean = get_pal_mean(c_sedentary_rate, c_met_mean, c_met_mvpa, c_met_non_mvpa) 
	
	b_fac = b_energy_mean/b_pal_mean 
	c_fac = c_energy_mean/c_pal_mean 

	fac5 = b_height_mean * b_height_mean 
	if ismale:
		fac6 = para1 * para2_m * (c_fac - b_fac) / fac5
	else:
		fac6 = para1 * para2_f * (c_fac - b_fac) / fac5
	bmi_counterfactual_mean = b_bmi_mean + fac6 
	return bmi_counterfactual_mean

def get_pal_mean(sedentary_rate, met_mean, met_mvpa, met_non_mvpa):
	pal_sedentary 	= get_pal_sedentary(met_non_mvpa)
	pal_active	= get_pal_active(met_mean, met_mvpa, met_non_mvpa)
	fac1 		= sedentary_rate/100.0
	fac3		= 1.0 - fac1
	fac2		= fac1 * pal_sedentary
	fac4		= fac3 * pal_active 
	pal_mean = fac2 + fac4
	return pal_mean

def get_pal_sedentary(met_mvpa):
	pal_sedentary = met_mvpa * 24 / 24
	return pal_sedentary
	
def get_pal_active(met_mean, met_mvpa, met_non_mvpa):
	fac1 = met_mean/7.0
	fac2 = (24.0 - (met_mean/(met_mvpa*7.0))) * met_non_mvpa
	pal_active = (fac1 + fac2)/24.0
	return pal_active
	
