# README

## Django apps

### faq app

- app for FAQ section

### news app

- app for News section


### prime app

- prime/ 
	- The *configuation_root* of the project.  
	- Project-wide settings, urls.py and wsgi.py modules.
	
	- templates/ 	
		- Site-wide Django templates
	- static/
		- Non-user-generated static media assets, including CSS, JavaScript and images
	- profiles/
		- App for managing and displaying user profiles

### primemodel app

- primemodel/ 	
	- App for managing and processing data in the PRIME model
	
### publications app

- app for Publications section

## Libraries *(not apps)*
- common/
	- Shared code / helper functions etc…
	- Libarary of functions stored in *utils.py*
	- e.g. iround() - function to round decimal/float to the nearers whole number 
- primelogic/
	- Logic for the PRIME model 
