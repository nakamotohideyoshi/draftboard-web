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

# Remove password from default postgres user
sudo -u postgres psql template1 -x -c "ALTER ROLE postgres PASSWORD ''"
# Set postgres configuration
cp /vagrant/site-setup/postgresql.conf /etc/postgresql/9.3/main/postgresql.conf
# Since we only use this box for development, open up all connections to the world.
cp /vagrant/site-setup/pg_hba.conf /etc/postgresql/9.3/main/pg_hba.conf
# Restart postgres to reload configurations
service postgresql restart

apt-get install -y git

#
# create postgres user 'vagrant'
cd /vagrant
./site-setup/createuser_vagrant.sh

#
# create the 'dfs' database, and give 'vagrant' the necessary permissions for postgres stuff
./site-setup/create_db_dfs.sh      # perform the last 4 commands

#
# Install redis + add configuration file.
apt-get install -y redis-server=2:2.8.4-2
cp /vagrant/site-setup/redis.conf /etc/redis/redis.conf


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

# Set vagrant user as the owner for the new virtualenv
# It was created by sudo, but vagrant needs to be the owner.
chown -R vagrant:vagrant /home/vagrant/venv

# Activate the virtual env.
source venv/bin/activate

#
# this global package will be required before you can use pip3 to install psycopg2
apt-get build-dep -y psycopg2

#
# install django and the basic things it needs...
    #<<<<<<< HEAD
    #venv/bin/pip3 install -r /vagrant/requirements/local.txt
    #
    ## Add an environment variable to tell django to always use the local settings by default.
    #echo "export DJANGO_SETTINGS_MODULE=mysite.settings.local" >> /home/vagrant/.bashrc
    #
    ## Activate the virtualenv on every login
    #echo "source venv/bin/activate" >> /home/vagrant/.bashrc
    #=======
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
venv/bin/pip3 install django-suit
venv/bin/pip3 install django-braces
venv/bin/pip3 install testfixtures

#
# we will need this for ssl stuff (including python paypal sdk)
apt-get install libssl-dev libffi-dev
#venv/bin/pip3 install paypalrestsdk

#apt-get install redis-server           #installed above
venv/bin/pip3 install django-redis
venv/bin/pip3 install django-celery
    #>>>>>>> 30e843f782ed8651ae0e562d73221396a1afc0eb

#
# we will need a webserver of course, and drop in our nginx server conf file & restart
#apt-get install -y nginx
#cp /vagrant/site-setup/nginx-default /etc/nginx/sites-available/default        # websrv/nginx-default is a simple server{}
#service nginx restart

    #<<<<<<< HEAD
    ## TODO: these still fail for me, not quite sure why, something about django's database configuration.
    #=======
    ##
    ## switch to user 'vagrant' because manage.py doesnt like connecting to postgres otherwise
    #>>>>>>> 30e843f782ed8651ae0e562d73221396a1afc0eb
cd /vagrant
./site-setup/migrate_and_syncdb.sh
