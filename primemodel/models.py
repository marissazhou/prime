from django.db import models
from django.contrib.auth.models import User

# Defined populations - initial baseline data is UK2007
# owner field allows for identification of own datasets in more advanced versions
class Population(models.Model):
	name 		= models.CharField(max_length=255, unique=True)
	owner		= models.ForeignKey(User, default=1)
	created_at	= models.DateTimeField(auto_now_add=True)
	updated_at	= models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['pk']

# Population subsets - e.g. Males aged 15-19 within the UK2007 population dataset
class PopulationSubset(models.Model):
	population 	= models.ForeignKey(Population, default=1)
	age_group	= models.CharField(max_length=10)
	gender		= models.CharField(max_length=1)
	size		= models.IntegerField(default=0)
	created_at	= models.DateTimeField(auto_now_add=True)
	updated_at	= models.DateTimeField(auto_now=True)

	#Something strange going on here... error is: 'tuple' object has no attribute 'encode'
	@property
	def fullname(self):
		return '%s::%s::%s' % (self.population, self.age_group, self.gender)

	class Meta:
		unique_together = ('population', 'age_group', 'gender')
		ordering 	= ['pk']

	def __unicode__(self):
		return self.fullname

# Groups of Outcomes
class OutcomeGroup(models.Model):
	name 		= models.CharField(max_length=100)
	code 		= models.CharField(max_length=10)
	shortname 	= models.CharField(max_length=100)
	created_at	= models.DateTimeField(auto_now_add=True)
	updated_at	= models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['pk']


# e.g. all diseases, but set to 'Outcome' rather than 'Disease' in order to maintain flexibility
class Outcome(models.Model):
	name 			= models.CharField(max_length=100, null=True) 
	outcomegroup 	= models.ForeignKey(OutcomeGroup, null=True) 
	shortname		= models.CharField(max_length=100, null=True)
	icd10_name 		= models.CharField(max_length=100)
	icd10_code		= models.CharField(max_length=20)
	owner 			= models.ForeignKey(User, default=1)
	created_at		= models.DateTimeField(auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)
	abbreviation		= models.CharField(max_length=20)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['pk']

# Baseline mortality rates for individual diseases/outcomes within population subsets
class Mortality(models.Model):
	population_subset 		= models.ForeignKey(PopulationSubset)
	outcome 			= models.ForeignKey(Outcome)
	value 				= models.IntegerField(default=0)
	owner 				= models.ForeignKey(User, default=1)
	created_at			= models.DateTimeField(auto_now_add=True)
	updated_at			= models.DateTimeField(auto_now=True)

	@property
	def fullname(self):
		return '%s::%s' % (self.population_subset, self.outcome)

	def __unicode__(self):
		return self.fullname

	class Meta:
		verbose_name_plural = 'mortalities'
		ordering = ['pk']

# References upon which the parameters are based
class Reference(models.Model):
	meta_analysis_ref		= models.TextField('Ref.', null=True)
	meta_analysis_ref_url		= models.URLField('Ref URL', max_length=255, null=True, blank=True)
	title				= models.TextField(max_length=255, null=True, blank=True)
	authors 			= models.TextField(max_length=255, null=True, blank=True)
	journal_name 			= models.TextField(max_length=255, null=True, blank=True)
	volume_number			= models.TextField(max_length=255, null=True, blank=True)
	year_published			= models.TextField(max_length=255, null=True, blank=True)
	page_numbers			= models.TextField(max_length=255, null=True, blank=True)
	details				= models.TextField(max_length=255, null=True, blank=True)
	abstract 			= models.TextField(max_length=255, null=True, blank=True) 
	owner 				= models.ForeignKey(User, default=1)
	created_at			= models.DateTimeField(auto_now_add=True)
	updated_at			= models.DateTimeField(auto_now=True)

	@property
	def shortname(self):
		return self.meta_analysis_ref[:25]

	def __unicode__(self):
		return self.shortname

	class Meta:
		ordering = ['pk']

# e.g. Diet, PA, Obesity, Alohol Consumption, Smoking
class ExposureGroup(models.Model):
	name 		= models.CharField(max_length=255)
	owner 		= models.ForeignKey(User, default=1)
	created_at	= models.DateTimeField(auto_now_add=True)
	updated_at	= models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['pk']

# e.g. Energy intake, Fibre 
class Exposure(models.Model):
	name 			= models.CharField('Exposure', max_length=255)
	exposure_group 		= models.ForeignKey(ExposureGroup) 
	dist_type		= models.CharField(max_length=11)
	owner 			= models.ForeignKey(User, default=1)
	created_at		= models.DateTimeField(auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['pk']

# e.g. CHD relative risk per 106g increase in fruit intake:
# 	Has mean, SD, CI high etc... 
class ExposureDistribution(models.Model):
	name 				= models.TextField()
	x_mean 				= models.DecimalField('_Mean_', max_digits=19, decimal_places=9, null=True)
	x_sd 				= models.DecimalField('_Mean_', max_digits=19, decimal_places=9, null=True)
	distribution_type 		= models.CharField('Dist. type', max_length=100, null=True)
	randomised_estimate		= models.DecimalField('Random. est.', max_digits=19, decimal_places=9, null=True)
	ci_low				= models.DecimalField('CI high', max_digits=19, decimal_places=9, null=True)
	ci_high				= models.DecimalField('CI low', max_digits=19, decimal_places=9, null=True)
	mean				= models.DecimalField('Mean', max_digits=19, decimal_places=9, null=True)
	sd				= models.DecimalField('SD', max_digits=19, decimal_places=9, null=True)
	original_estimate		= models.DecimalField('Orig. est.', max_digits=19, decimal_places=9, null=True)
	lower_estimate_limit		= models.DecimalField('Low limit', max_digits=19, decimal_places=9, null=True)
	upper_estimate_limit		= models.DecimalField('Up limit', max_digits=19, decimal_places=9, null=True)
	reference 			= models.ForeignKey(Reference, null=True, blank=True)
	owner 				= models.ForeignKey(User, default=1)
	created_at			= models.DateTimeField(auto_now_add=True)
	updated_at			= models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['pk']

# Types of measurement - e.g. Mean Fibre/day, SD Fibre/day... 
class MeasurementType(models.Model):
	name 				= models.CharField(max_length=255)
	exposure 			= models.ForeignKey(Exposure)
	MEAN 				= 'Mean'
	SD 				= 'SD'
	PERCENTAGE 			= 'Percentage'
	OTHER 				= 'Other'
	STATISTICAL_OPTIONS = 	(
								(MEAN, 'Mean'),
								(SD, 'Standard Deviation'),
								(PERCENTAGE, 'Percentage of Population'),
								(OTHER, 'Other'),
							)
	statistical_measure = models.CharField(max_length=20, choices=STATISTICAL_OPTIONS)
	unit 				= models.CharField(max_length=20)
	owner 				= models.ForeignKey(User, default=1)
	created_at			= models.DateTimeField(auto_now_add=True)
	updated_at			= models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.id

	class Meta:
		ordering = ['pk']

# Baseline measurements (e.g. value for the Mean Fibre/day for UK2007 male 15-19)
# This is to show in the admin
class Measurement(models.Model):
	measurement_type 		= models.ForeignKey(MeasurementType)
	population_subset 		= models.ForeignKey(PopulationSubset)
	BASELINE 			= 'B'
	COUNTERFACTUAL 			= 'C'
	MEASUREMENT_OPTIONS 		= 	(
									(BASELINE, 'Baseline'),
									(COUNTERFACTUAL, 'Counterfactual'),
								) 
	measurement_option 		= models.CharField(max_length=1, choices=MEASUREMENT_OPTIONS)
	value 				= models.DecimalField(max_digits=19, decimal_places=9, null=True)
	owner 				= models.ForeignKey(User, default=1)
	created_at			= models.DateTimeField(auto_now_add=True)
	updated_at			= models.DateTimeField(auto_now=True)

	@property
	def fullname(self):
		return '%s::%s' % (self.population_subset, self.measurement_type)

	class Meta:
		unique_together = ('population_subset', 'measurement_type', 'measurement_option')
		ordering 	= ['pk']

	def __unicode__(self):
		return self.fullname

# Exposure bins 
class ExposureBins(models.Model):
	exposure 				= models.ForeignKey(Exposure)
	bin_type				= models.CharField(max_length=11, null=True, blank=False)
	bin_value				= models.DecimalField(max_digits=19, decimal_places=9)

	@property
	def name(self):
		return '%d' % (self.bin_value) 

	def __unicode__(self):
		return self.id

	class Meta:
		ordering = ['pk']


# Relative risk values, defined from the literature.  
# Equivalent to the black-outline yellow boxes in the relative risk section of the Excel model
# Current need to be added by hand
class RelativeRisk(models.Model):
	exposure 			= models.ForeignKey(Exposure)
	population_subset 		= models.ForeignKey(PopulationSubset)
	outcome				= models.ForeignKey(Outcome)
	exposure_distribution 		= models.ForeignKey(ExposureDistribution, null=True)
	bin_value			= models.ForeignKey(ExposureBins, null=True)
	risk_value			= models.DecimalField(max_digits=29, decimal_places=19)
	owner 				= models.ForeignKey(User, default=1)
	created_at			= models.DateTimeField(auto_now_add=True)
	updated_at			= models.DateTimeField(auto_now=True)

	@property
	def name(self):
		return '%s::%s::%s' % (self.exposure, self.outcome, self.population_subset) 

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['pk']

# Exposure Outcome association
class ExposureOutcome(models.Model):
	exposure 				= models.ForeignKey(Exposure)
	outcome 				= models.ForeignKey(Outcome)
	lower_limit_estimate			= models.DecimalField(max_digits=19, decimal_places=9)
	upper_limit_estimate 			= models.DecimalField(max_digits=19, decimal_places=9)
	measure					= models.DecimalField(max_digits=19, decimal_places=9)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['pk']

# all test data from Anja's test file 
class TestParameter(models.Model):
	total_energy_mean			= models.DecimalField(max_digits=19, decimal_places=9)
	fruit_mean				= models.DecimalField(max_digits=19, decimal_places=9)
	fruit_sd 				= models.DecimalField(max_digits=19, decimal_places=9)
	fruit_non_rate				= models.DecimalField(max_digits=19, decimal_places=9)
	veg_mean				= models.DecimalField(max_digits=19, decimal_places=9)
	veg_sd	 				= models.DecimalField(max_digits=19, decimal_places=9)
	veg_non_rate				= models.DecimalField(max_digits=19, decimal_places=9)
	fibre_mean				= models.DecimalField(max_digits=19, decimal_places=9)
	fibre_sd 				= models.DecimalField(max_digits=19, decimal_places=9)
	salt_mean				= models.DecimalField(max_digits=19, decimal_places=9)
	salt_sd 				= models.DecimalField(max_digits=19, decimal_places=9)
	total_fat_mean				= models.DecimalField(max_digits=19, decimal_places=9)
	total_fat_sd 				= models.DecimalField(max_digits=19, decimal_places=9)
	saturate_fat_mean			= models.DecimalField(max_digits=19, decimal_places=9)
	saturate_fat_sd				= models.DecimalField(max_digits=19, decimal_places=9)
	mufa_fat_mean				= models.DecimalField(max_digits=19, decimal_places=9)
	mufa_fat_sd				= models.DecimalField(max_digits=19, decimal_places=9)
	pufa_fat_mean				= models.DecimalField(max_digits=19, decimal_places=9)
	pufa_fat_sd 				= models.DecimalField(max_digits=19, decimal_places=9)
	dietary_cholesterol_mean		= models.DecimalField(max_digits=19, decimal_places=9)
	dietary_cholesterol_sd	 		= models.DecimalField(max_digits=19, decimal_places=9)
	met_mean				= models.DecimalField(max_digits=19, decimal_places=9)
	met_sd 					= models.DecimalField(max_digits=19, decimal_places=9)
	sedentary_rate				= models.DecimalField(max_digits=19, decimal_places=9)
	met_non_mvpa				= models.DecimalField(max_digits=19, decimal_places=9)
	met_mvpa				= models.DecimalField(max_digits=19, decimal_places=9)
	alcohol_low				= models.DecimalField(max_digits=19, decimal_places=9)
	alcohol_mean				= models.DecimalField(max_digits=19, decimal_places=9)
	alcohol_sd 				= models.DecimalField(max_digits=19, decimal_places=9)
	smoker_never				= models.DecimalField(max_digits=19, decimal_places=9)
	smoker_previous				= models.DecimalField(max_digits=19, decimal_places=9)
	smoker_current				= models.DecimalField(max_digits=19, decimal_places=9)
	result					= models.DecimalField(max_digits=19, decimal_places=9)

	class Meta:
		ordering = ['pk']
