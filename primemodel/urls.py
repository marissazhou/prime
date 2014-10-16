from django.conf.urls import patterns, include, url

urlpatterns = patterns('primemodel.views',
    url(r'^$', 'index'),
    url(r'^hw/$', 'hello_world'),
    url(r'^pops$', 'population_subset'),
    url(r'^testprime$', 'test_prime'),
    url(r'^testboost$', 'testboost'),
    # localhost:8000/prime/distribution/fibre -> start here!
    url(r'^distribution/(\w+)$', 'distribution'),
    # using class-based-views this is:
    # url(r'^exposure/$', Exposure.as_view()),
    #url(r'^exposure/(?P<factor>\w+)$', Exposure.as_view()),
    url(r'^return_json_data$', 'return_json_data'),
    url(r'^parameters/set$', 'set_parameters'),
    url(r'^parameters/mean/(?P<mean>\d+)/sd/(?P<sd>\d+)', 'stats'),
    (r'^prime/(\d{4})/(\d{2})/(\d+)/$', 'refresh_counterfactual_url'), 
    # """
    # Following URL receives new counterfactual changes from url changes and react to the changes 
    # e.g. 'http://localhost:8000/prime/o/?exposure=Fruit&mean=200&standard-deviation=15.5&non-rate=0/'
    #     - 'o' = 'only' (i.e. single exposure)
    #     - 'c' = 'compound' (i.e. multiple exposures)
    # """ 
    (r'^(\w{1})/$', 'refresh_counterfactual_url_type'), 
    # """
    # Following URL directs to function which looks at JSON file with compound (or single) exposure
    # Currently the JSON is hardcoded in the function 
    # """
    (r'^(\w+)/$', 'refresh_counterfactual_url_json'), 
    url(r'^refresh_counterfactual_json$', 'refresh_counterfactual_json'),
)
