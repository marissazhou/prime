import datetime

from django.http import HttpResponse
from django.views.generic.base import View
from django.template import loader, Context
from django.shortcuts import render_to_response, get_object_or_404
import json
from django.core.context_processors import csrf
#import pdb; pdb.set_trace()

from primemodel.models import *
from primemodel.prime import *
from primemodel.forms import BasicForm

from primemodel.logic import * 
from primemodel.utils import * 
from primemodel.DBHelper import DBHelper 
from primemodel.PrimeExposure import PrimeExposure 
from primemodel.PrimeCoordinator import PrimeCoordinator 
from primemodel.PopDistribution import PopDistribution 
from primemodel.PrimeOutcome import PrimeOutcome 


primeCoordinator = PrimeCoordinator() #initiate an PrimeCoordinator object

def getpopulations(gender='M', limit=10):
	populations 		= Population.objects.all().order_by('created_at')[:limit]
	return populations

def getvariables():
	subsets = Variable.objects.all().order_by('created_at')
	return subsets

def getsubsets():
	subsets = PopulationSubset.objects.all().order_by('created_at')
	return subsets
#################################################
	# outcomes
	#################################################
def get_exposure(exposure_id,b_mean,b_sd,c_mean,c_sd,non_rate,dist_type,mortalities):#id in db
	"""This function translates foo into bar

    	:param exposure_id: id for exposures
    	:param b_mean: mean for baseline 
    	:param b_sd: standard deviation for counterfactual 
    	:param c_mean: mean for baseline 
    	:param c_sd: standard deviation for counterfactual 
    	:param non_rate: non rate for smokers/drinkers 
    	:param dist_type: distribution type 
   	:param mortalities: baseline mortalities for a new exposure

    	:returns: a list of initial/baseline exposures 
    	"""
	e_id 		= int(long(exposure_id))
	exposure_outcomes = DBHelper.exposure_outcome
	outcome_ids 	= DBHelper.exposure_outcome.get(e_id)

	samples_rr 	= DBHelper.samples_rr.get(e_id)
	samples_pop 	= DBHelper.samples_pop.get(e_id)
	risks 		= DBHelper.risks.get(e_id)
	measure 	= DBHelper.measures.get(e_id)
	dist_type   	= get_dist_type(e_id)

	#get population distribution 
	popDistribution = PopDistribution(DBHelper.age_group_num,non_rate,b_mean,b_sd,c_mean,c_sd,samples_pop,dist_type)

	#get outcomes
	outcomes = []
	for o_id in outcome_ids:
		# mortality
		m_mortality = mortalities.get(2*o_id)
		f_mortality = mortalities.get(2*o_id+1)
		# risks
		m_risks = risks.get(2*o_id)
		f_risks = risks.get(2*o_id+1)
		# outcome name
		name = DBHelper.get_outcome_name(o_id)
		# limit estimates
		lle = DBHelper.exposure_outcome.get(e_id).get(o_id)[0]
		ule = DBHelper.exposure_outcome.get(e_id).get(o_id)[1]
		# outcome
		outcome = PrimeOutcome(name,o_id,m_mortality,f_mortality,samples_rr,m_risks,f_risks,lle,ule,measure,e_id) 
		outcomes.append(outcome)

	exposure = PrimeExposure(mortalities,outcome_ids,samples_rr,samples_pop,outcomes,popDistribution)
	return exposure

def hello_world(request):
	return HttpResponse("Hwello Wrold")

def testboost(request):
	template = loader.get_template('primemodel/testboost.html')
	para_view = {}
	context = Context(para_view)
	response = template.render(context)
	return HttpResponse(response)

def index(request):
	template = loader.get_template('primemodel/index.html')
	para_view = {}
	context = Context(para_view)
	response = template.render(context)
	return HttpResponse(response)

def refresh_counterfactual_url(request):
	template = loader.get_template('primemodel/index.html')
	para_view = {}
	context = Context(para_view)
	response = template.render(context)
	return HttpResponse(response)

def refresh_index_page_filter_by(request, exposure_sequence):
	"""Refresh user page when user clicks show-by 
   	:returns: 
	"""	
		
def refresh_counterfactual_url_json(request, is_json):
	"""This function receives new counterfactual changes from json changes and react to the changes 
	   json format should be {['e_id':1,'non_rate':9,'mean':1,'sd':1]}

   	:returns: calculating counterfactual mortalities for new parameter settings, and refresh prime index page with new counterfactual parameters
	"""	
	if is_json != 'json':
		return

        #json_file = '/home/zhou/Downloads/jsons/only/json_7.json'
        json_file = '/home/zhou/Downloads/jsons/compound/json_9.json'
	#json_file = '/Users/jiaozi/Downloads/jsons/compound/json_2.json' #json file address
        exposure_sequence = read_json(json_file)#list of exposures{mean,sd,non_rate}, read json content into memory

	primeCoordinator.get_counterfactual_compound_exposures(exposure_sequence)
	

	'''
		For interface output data format, please refer to refresh_output_counterfactual_mortality. When a user clicks on age/gender/outcome, he can view mortalities in different formats
                It refreshes final compound mortality for output, it should be the counterfactual mortality of the final exposure.
                        In order to show mortality by age/outcome/gender, there should be three lists.
                        1. Show by age/population_subset 
                                All information to present on a webpage is stored in variable 'output_all_mortality_exposure_age', the format of this variable is [{'population_subset_id':1,'age_group':'15-19','b_mortality_sum_db':757,'c_mrtality_sum':341}] 
                        2. Show by outcome 
                                All information to present on a webpage is stored in variable 'output_all_mortality_exposure_outcome', the format of this variable is [{'o_id':1,'name':'Stroke','b_mortality_sum_db':24757,'c_mrtality_sum':23415}] 
                        3. Show by gender 
                                All information to present on a webpage is stored in variable 'output_all_mortality_exposure_gender', the format of this variable is [{'gender':'male','b_mortality_sum_db':24757,'c_mrtality_sum':415}] 

	'''
	#filter_by	= request.POST['filter-by'] 
	filter_by	= request.GET
	by		= request.POST
	print filter_by
	print by

	# get the data in the interface
	b_output_mortality 	= primeCoordinator.output_baseline_mortality
	b_output_mortality_num 	= primeCoordinator.output_baseline_mortality_num
	b_total_mortality 	= primeCoordinator.output_baseline_mortality_total
	c_output_mortality 	= primeCoordinator.output_counterfactual_mortality
	c_output_mortality_num 	= primeCoordinator.output_counterfactual_mortality_num
	c_total_mortality 	= primeCoordinator.output_counterfactual_mortality_total
	total_population	= primeCoordinator.output_total_population
	total_death_averted	= str(int(round(primeCoordinator.output_total_death_averted))) # int
	#total_death_averted	= str(primeCoordinator.output_total_death_averted) # decimale
	total_death_baseline	= str(primeCoordinator.output_total_death_baseline)

	'''
		This is the outputs when user click outcome
	'''
	all_mortality_exposure	= primeCoordinator.output_all_mortality_exposure_outcome # [{'outcome_id':outcome_id,'name':outcome name,'baseline_death':100, 'counterfactual_death':20},{}] 

	'''
		This is the output when user click age
	'''
	all_mortality_age	= primeCoordinator.output_all_mortality_age # [{'age_group_id':age_group_id,'age_group':age_group,'baseline_death':100, 'counterfactual_death':20},{}] 

	'''
		This is the outputs when user click gender 
	'''
	all_mortality_gender	= primeCoordinator.output_all_mortality_gender# [{'gender':'male','baseline_death':100, 'counterfactual_death':20},{'gender':'female','baseline_death':100, 'counterfactual_death':20}] 


	#transmit the parameters
	template = loader.get_template('primemodel/index.html')
	para_view = {
			'b_output_mortality_num':	b_output_mortality_num,
			'b_total_mortality':		b_total_mortality,
			'c_output_mortality_num':	c_output_mortality_num,
			'c_total_mortality':		c_total_mortality,
			'total_population':		total_population,
			'total_death_averted':		total_death_averted,
			'total_death_baseline':		total_death_baseline,
			'all_mortality_exposure':	all_mortality_exposure
			}

	#context to transmit the parameters to show
	context = Context(para_view)
	response = template.render(context)
	return HttpResponse(response)


def refresh_counterfactual_url_type(request, compound_type):
	"""This function receives new counterfactual changes from url changes and react to the changes 
	   url should be 'http://localhost:8000/prime/o/?exposure=Fruit&mean=200&standard-deviation=15.5&non-rate=0/'

    	:param compound_type: 'o' means 'only' for 'only exposures', 'c' means 'compound' for 'compound exposures' 
    	:type compound_type: char 
   	:returns: calculating the final counterfactual mortalities, and refresh prime index page with new counterfactual parameters
	"""	

	now = datetime.datetime.now()
	print "Start Time %s" % now

	c_type 		= compound_type 	# compound type, o to be only and c to be compound
	primeCoordinator= PrimeCoordinator() 	# initiate an PrimeCoordinator object to manipulate inputed parameters to get a counterfactual results

	now = datetime.datetime.now()
	print "Coordinator initialised %s" % now

	# Get variables from URL and create array
	exposure_name 		= request.GET.get('exposure', '')
	e_id 			= DBHelper.get_exposure_id_from_name(exposure_name)
	mean 			= request.GET.get('mean', '')
	sd   			= request.GET.get('standard-deviation', '')
	non_rate		= request.GET.get('non-rate', '')
	exposure_sequence 	= [{'non_rate':non_rate,'mean':mean,'e_id':e_id,'sd':sd}]

	primeCoordinator.get_counterfactual_compound_exposures(exposure_sequence)

	now = datetime.datetime.now()
	print "Coordinator given exposures %s" % now

	# get the data in the interface
	b_output_mortality 	= primeCoordinator.output_baseline_mortality # baseline mortality list for all outcomes
	b_output_mortality_num 	= primeCoordinator.output_baseline_mortality_num # baseline mortality sum up for each outcome
	b_total_mortality 	= primeCoordinator.output_baseline_mortality_total# baseline mortality sum up for all outcomes

	now = datetime.datetime.now()
	print "Total baseline mortality calculated %s" % now

	c_output_mortality 	= primeCoordinator.output_counterfactual_mortality# counterfactual mortality for all outcomes
	c_output_mortality_num 	= primeCoordinator.output_counterfactual_mortality_num# counterfactual mortality for each outcome
	c_total_mortality 	= primeCoordinator.output_counterfactual_mortality_total# counterfactual mortality sum up for all outcomes

	now = datetime.datetime.now()
	print "Total counterfactual mortality calculated %s" % now

	total_population	= primeCoordinator.output_total_population
	all_mortality_exposure	= primeCoordinator.output_all_mortality_exposure_outcome

	now = datetime.datetime.now()
	print "Total deaths averted calculated %s" % now

	total_death_averted	= str(round(primeCoordinator.output_total_death_averted,0))
	total_death_baseline	= str(primeCoordinator.output_total_death_baseline)


	now = datetime.datetime.now()
	print "End Time: %s" % now

	#transmit the parameters
	template = loader.get_template('primemodel/index.html')
	para_view = {
			'b_output_mortality_num':	b_output_mortality_num,
			'b_total_mortality':		b_total_mortality,
			'c_output_mortality_num':	c_output_mortality_num,
			'c_total_mortality':		c_total_mortality,
			'total_population':			total_population,
			'total_death_averted':		total_death_averted,
			'total_death_baseline':		total_death_baseline,
			'all_mortality_exposure':	all_mortality_exposure
			}

	#context to transmit the parameters to show
	context = Context(para_view)
	response = template.render(context)
	return HttpResponse(response)

def refresh_counterfactual_json(request):
	"""This function receives new counterfactual changes from json changes and react to the changes 

    	:param :
    	:type : 
   	:returns: calculating , and refresh prime index page with new counterfactual parameters
	 """	


        """
                the following json are for compound exposures
        """
        #json_file = '/home/zhou/Downloads/jsons/compound/json_9.json'
	json_file = '/Users/jiaozi/Downloads/jsons/compound/json_9.json'

        exposure_sequence = read_json(json_file)#list of exposures{mean,sd,non_rate}

	primeCoordinator = PrimeCoordinator()
	primeCoordinator.get_counterfactual_compound_exposures(exposure_sequence)
	
	# get the data in the interface
	b_output_mortality 	= primeCoordinator.output_baseline_mortality # baseline mortality list for all outcomes
	b_output_mortality_num 	= primeCoordinator.output_baseline_mortality_num # baseline mortality sum up for each outcome
	b_total_mortality 	= primeCoordinator.output_baseline_mortality_total# baseline mortality sum up for all outcomes
	c_output_mortality 	= primeCoordinator.output_counterfactual_mortality# counterfactual mortality for all outcomes
	c_output_mortality_num 	= primeCoordinator.output_counterfactual_mortality_num# counterfactual mortality for each outcome
	c_total_mortality 	= primeCoordinator.output_counterfactual_mortality_total# counterfactual mortality sum up for all outcomes
	total_population	= primeCoordinator.output_total_population
	all_mortality_exposure	= primeCoordinator.output_all_mortality_exposure
	total_death_averted	= str(round(primeCoordinator.output_total_death_averted,0))
	total_death_baseline	= str(primeCoordinator.output_total_death_baseline)

	#transmit the parameters
	template = loader.get_template('primemodel/index.html')
	para_view = {
			'b_output_mortality_num':	b_output_mortality_num,
			'b_total_mortality':		b_total_mortality,
			'c_output_mortality_num':	c_output_mortality_num,
			'c_total_mortality':		c_total_mortality,
			'total_population':		total_population,
			'total_death_averted':		total_death_averted,
			'total_death_baseline':		total_death_baseline,
			'all_mortality_exposure':	all_mortality_exposure
			}

	#context to transmit the parameters to show
	context = Context(para_view)
	response = template.render(context)
	return HttpResponse(response)

def population_subset(request):
	subsets = getsubsets()
	response = '''
	<html>
		<head>
			<title>PRIME</title>
		</head>
		<body>
			<ul>
			%s
			</ul>
		</body>
	</html>
	''' % '\n' . join(['<li>%s</li>' % subset.population for subset in subsets])

	return HttpResponse(response)

def test_prime(request):
	variables = get_variables()
	template = loader.get_template('primemodel/test_prime.html')
	context = Context({'variables': variables})
	response = template.render(context)
	return HttpResponse(response)

def distribution(request, variable):
	# variable = 'fibre'
	data = get_baseline_stats(variable)
	# template = loader.get_template('primemodel/distribution.html')
	# context = Context({'variable': baseline_stats})
	# response = template.render(context)
	return HttpResponse(json.dumps(data), mimetype='application/json')

def return_json_data(request):
	data = {'a': 'A', 'b': (2,4), 'c': 3.0}
	return HttpResponse(json.dumps(data), mimetype='application/json')

def set_parameters(request):
	if request.method == 'POST':
		print "IN POST"
		form = BasicForm(request.POST)
		if form.is_valid():
			mean = form.cleaned_data['mean']
			sd = form.cleaned_data['sd']
			return http.HttpResponseRedirect('/prime/parameters/mean/%s/sd/%s' % (mean, sd))

	else:
		form 	= BasicForm()
		print "IN GET"
	
	context = Context({'title': 'Test Form', 'form': form})
	context.update(csrf(request))
	return render_to_response('primemodel/set_parameters.html', context)

def stats(request, mean, sd):	
	context = Context({'title': 'Showing Stats', 'mean': mean, 'sd': sd})
	return render_to_response('primemodel/showstats.html', context)

# Parent class for the PRIME model... everything based from here
# Keep these classes 'skinny' -> delegate work to the 'prime.py' or 'primelogic/logic.py' libraries (which need to be merged or separated sensibly)
class Exposure(View):
#
	# variable = 'needs to be set by URL' # This will be set by the URL call - throw error if blank
	factor = 'set by URL'

	def get(self, request, *args, **kwargs):

		# Get the factor that we're interested in for basic manipulation
		self.factor = self.kwargs['factor']

		# Use 'factor' to get baseline statistics
		data = get_baseline_stats(self.factor)

		# Return JSON with data 
		return HttpResponse(json.dumps(data), mimetype='application/json')

# All the basic variables - e.g. fibre.  
# May not need this - may be able to just create objects directly from Exposure class
class BasicExposure(Exposure):
	pass

class ComplexExposure(Exposure):
	pass

class CompoundExposure(Exposure):
	pass

