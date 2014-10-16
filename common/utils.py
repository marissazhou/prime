import scipy.stats

# Round to nearest whole number
def iround(x):
	y = round(x) - .5
	return int(y) + (y > 0)

# Calculate baseline distribution
def calc_baseline_dist(mean,sd,pop,upper,lower):
	value = pop*(scipy.stats.norm(mean,sd).cdf(upper) - scipy.stats.norm(mean,sd).cdf(lower))
	value = iround(value)
	return value
