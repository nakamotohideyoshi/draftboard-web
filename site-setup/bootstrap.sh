#!/usr/bin/env bash

############## notes #########################################################
### 0.  everything is run as 'sudo' so its not explicitly used in this script
### 1.  use 'pip3' not 'pip'   !!
### 2.  use 'python3' not 'python'    !!
### 3. 	this script executes from /home/vagrant 	but your code should be in /vagrant !						
### 4. 	"-y" flag to apt-get commands automatically says 'y' to prompts
##############################################################################

apt-get update
#apt-get install -y vim 	# already installed on base VM

#
#################################################################
#     				db setup
#################################################################
apt-get install -y postgresql

#
# create postgres user 'vagrant'
cd /vagrant
./site-setup/createuser_vagrant.sh

#
# create the 'dfs' database, and give 'vagrant' the necessary permissions for postgres stuff
./site-setup/create_db_dfs.sh      # perform the last 4 commands

#
#apt-get install -y python-setuptools 		# a dependency for many python things
apt-get install -y python3-setuptools 		# a dependency for many python things

#apt-get install -y python-pip
apt-get install -y python3-pip 				# installs 'pip3' utility


################### after you have pip3, you can install virtual env and set it up #############

#
# install virtualenv (should always do this for python projects)
pip3 install virtualenv

#
# setup the virtual environment before you install django and django stuff, or do a pip freeze 
cd /home/vagrant

virtualenv venv 		# create our virtual environment dir

#
# this global package will be required before you can use pip3 to install psycopg2
apt-get build-dep -y psycopg2

#
# install django and the basic things it needs...
venv/bin/pip3 install Django==1.8               # LTS April 1, 2015 (no foolin!)
venv/bin/pip3 install psycopg2
venv/bin/pip3 install gunicorn
venv/bin/pip3 install dj-database-url
venv/bin/pip3 install dj-static
venv/bin/pip3 install static
venv/bin/pip3 install djangorestframework    	# optional - for creating apis
venv/bin/pip3 install markdown 					# optional - for creating apis
venv/bin/pip3 install django-filter 			# optional - for creating apis
venv/bin/pip3 install sphinx 				    # !?  install in virtualenv. maybe do system-wide??
venv/bin/pip3 install braintree                 # payment processing
#venv/bin/pip3 install django_braintree          # third party braintree integration we might use

#
# we will need a webserver of course, and drop in our nginx server conf file & restart
apt-get install -y nginx
cp /vagrant/site-setup/nginx-default /etc/nginx/sites-available/default        # websrv/nginx-default is a simple server{}
service nginx restart

#
# switch to user 'vagrant' because manage.py doesnt like connecting to postgres otherwise
cd /vagrant
./site-setup/migrate_and_syncdb.sh
