How to Deploy
=============
This documentation describes how to deploy the prime model 

Software Requiremnts:
------------
In order to successfully run the prime model code, all following rerequisited packages/softwares are necessary to be installed beforehand.

- Django (1.5.4)
- django-bootstrap-staticfiles (3.0.0.1)
- django-bootstrap-toolkit (2.15.0)
- django-suit (0.2.5)
- ipython (1.1.0)
- matplotlib (1.3.0)
- MySQL-python (1.2.4)
- nose (1.3.0)
- numpy (1.7.1)
- pip (1.4.1)
- pip-tools (0.3.4)
- psycopg2 (2.5.1)
- pyparsing (2.0.1)
- python-dateutil (2.1)
- scipy (0.12.0)
- setuptools (0.9.8)
- six (1.4.1)
- tornado (3.1.1)
- wsgiref (0.1.2)

For Unbuntu 12.04 system, the commands for deployment:

- 
Refer to: https://docs.djangoproject.com/en/dev/topics/install/




To install MySQLdb module, download it from MySQLdb Download page and proceed as follows:
http://sourceforge.net/projects/mysql-python/

$ gunzip MySQL-python-1.2.2.tar.gz
$ tar -xvf MySQL-python-1.2.2.tar
$ cd MySQL-python-1.2.2
$ python setup.py build
$ python setup.py install

Install bootstrap 
-----------------
pip install -U django_bootstrap_staticfiles

Install suit
------------
pip install django-suit

Install numpy and scipy 
-------------
pip install numpy 
apt-get install python-numpy python-scipy

Install ipython 
---------------
pip install ipython 

Create database and import data
-------------------------------
- create an empty database name 'prime' in mysql
- run ./manage.py syncdb 
You just installed Django's auth system, which means you don't have any superusers defined.
Would you like to create one now? (yes/no): no
Select 'no' here!
- import data into database by running 'mysql -u primeuser -p prime < prime.sql'

Run in browser
--------------
Visit this url in the browser:
http://localhost:8000/prime/o/?exposure=Fruit&mean=200&standard-deviation=15.5&non-rate=0/
