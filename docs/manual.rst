.. highlight:: rst
.. highlight:: python 

Manual
=======================

This manual introduces how python coders and web users can use Prime Model API.

For Python Coder
----------------

user send parameter through json file or other formats like [exposureid:[mean,sd,non_rate],exposureid:[mean,sd,non_rate],]
.. code-block:: python
   [{
    "e_id": "1",
    "mean": "15.6",
    "sd": 25,    
    "non_rate": 25
    },
    {
    "e_id": "2",
    "mean": "3.6",
    "sd": 25,    
    "non_rate": 100
    }]

.. code-block:: python 

   #test on how to use ExposureController
   para = None # para is a list of counterfactual parameters
   eController = ExposureController(para)
   #get baseline and initial counterfactual exposures
   eController.get_initial_exposures()
   #new counterfactual exposures
   json_file = os.path.join(settings.PROJECT_PATH,'json.json')
   exposure_sequence = eController.read_json(json_file)#list of exposures{mean,sd,non_rate}
   eController.get_new_counterfactual_exposures(exposure_sequence)

   e1 = eController.get_attr_cc_exposure(0) # exposure_id
       
   # attributions death sum to show in the webpages
   outcomes_b_m_deaths_sum_e1        = e1.get_outcome_deaths_sum(0,True,True)

For Web Users
-------------
.. code-block:: python 

   url=http://
