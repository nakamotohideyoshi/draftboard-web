#!/usr/bin/env bash

############## notes #########################################################
### 0.  everything is run as 'sudo' so its not explicitly used in this script
### 1.  use 'pip3' not 'pip'   !!
### 2.  use 'python3' not 'python'    !!
### 3. 	this script executes from /home/vagrant 	but your code should be in /vagrant !
### 4. 	"-y" flag to apt-get commands automatically says 'y' to prompts
##############################################################################

#
######################################################################
#     				MongoDB (version >= 3.0.x)
######################################################################
cd /vagrant
./site-setup/install_mongo.sh
cp site-setup/mongod.conf /etc/mongod.conf      # make it use our conf file
service mongod stop                             # dont want the original running

#
#################################################################
#     				Java
#################################################################
# install oracle java 7 - we wil need this for DataDen primarily and the VM doesnt come with it
echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections
echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu precise main" | sudo tee /etc/apt/sources.list.d/webupd8team-java.list
echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu precise main" | sudo tee -a /etc/apt/sources.list.d/webupd8team-java.list
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EEA14886
apt-get update
apt-get install -y oracle-java7-installer
java -version    # output the version

#
######################################################################
#     				Postgres
######################################################################
apt-get install -y postgresql

# Remove password from default postgres user
sudo -u postgres psql template1 -x -c "ALTER ROLE postgres PASSWORD '';"
cd /vagrant
./site-setup/find_pg_hba.sh
service postgresql restart                  # restart postgres
./site-setup/createuser_vagrant.sh          # great the 'vagrant' user in postgres

#
# it will be useful to have git on the machine
apt-get install -y git

#
######################################################################
#     				Redis
######################################################################
apt-get install -y redis-server=2:2.8.4-2
cp /vagrant/site-setup/redis.conf /etc/redis/redis.conf

# start mongod daemon
# $> sudo service mongod start         # this may work, but we need to configure a replica set
mkdir /data
mkdir /data/db
#       cp /vagrant/site-setup/mongodb.conf /etc/mongodb/mongodb.conf
#       service mongod restart

# setuptools then pip - were using python3 for this project
apt-get install -y python3-setuptools 		# a dependency for many python things
apt-get install -y python3-pip 				# installs 'pip3' utility

# this global package will be required before you can use pip3 to install psycopg2
apt-get build-dep -y psycopg2
# that previous line installing psycopg2 may not have worked, so try the next line also
#pip3 install psycopg2

# install virtualenv (should always do this for python projects)
pip3 install virtualenv

#
# setup the virtual environment before you install django and django stuff, or do a pip freeze
cd /home/vagrant

virtualenv venv 		# create our virtual environment dir

# Set vagrant user as the owner for the new virtualenv
# It was created by sudo, but vagrant needs to be the owner.
chown -R vagrant:vagrant /vagrant
chown -R vagrant:vagrant /home/vagrant/venv

# Activate the virtual env.
source venv/bin/activate

#
# we will need this for ssl stuff (and potentially python paypal sdk)
apt-get install -y libssl-dev libffi-dev

#
# we will need a webserver of course, and drop in our nginx server conf file & restart
apt-get install -y nginx

# copy over a simple config that will enable us to hit django's runserver on localhost:8888
cp /vagrant/site-setup/nginx-default /etc/nginx/sites-available/default
service nginx restart

### get back to the project root before the following commands
cd /vagrant

#
# install django and everything in requirements/local.txt
cd /vagrant


pip3 install -r /vagrant/requirements/local.txt
##pip3 install optimal_source/src/

##
## manage.py migrate to install db tables and schema
./site-setup/migrate.sh

# install heroku toolbelt
wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh

#
# Add an environment variable to tell django to always use the local settings by default
#cat site-setup/etc_profile_add_django_settings_module.txt | sudo tee -a /etc/profile
echo "export DJANGO_SETTINGS_MODULE=mysite.settings.local" >> /home/vagrant/.bashrc

#
# Activate the virtualenv on every login
echo "source venv/bin/activate" >> /home/vagrant/.bashrc
echo "cd /vagrant" >> /home/vagrant/.bashrc

#
####################################################################
# potentially useful commands:
#
# start celery in terminal:
#   $> /home/vagrant/venv/bin/celery -A mysite worker -l info
#
# start mongo replica set (for dataden) in a terminal:
#   $> sudo mongod --replSet "rs0"
#       # you will need to login, and type the command 'rs.initialize()'
#
# start dataden.jar in a terminal:
#   $> java -jar dataden.jar -k YOUR_LICENSE_KEY
#
####################################################################

#
####################################################################
# ... and at this point you should be able to
#       ssh into the vagrant box and do djangos runserver.
#       Then you can hit the site from localhost:8888/admin/login/
#####################################################################

#
# in order to use dataden.jar and have mongo setup all you have to do is
# 1. Start mongo normally       :   sudo mongod
# 2. ctrl-c & start as replSet  :   sudo mongod --replSet "rs0"
# 3. log in to the mongo shell  :   mongo
# 4. type this in mongo shell   :   rs.initiate()


#
#####################################################################
# Tutorial on how to get NFL up from scratch (same for other sports)
#####################################################################
#
#    1) you have done a ./manage migrate successfully as a prerequisite
#
#    2) run dataden to pull stats into mongo (from root directory of project, ie: /vagrant)
#
#        $> java -jar dataden/dataden.jar -k <licenseKey>
#
#        $> ./manage.py shell
#        >>> from sports.parser import DataDenParser
#        >>> p = DataDenParser()
#        >>> p.setup_triggers('nfl')
#        >>> p.setup('nfl')                          # initializes teams, games, players + any playerstats for nfl
#
#        >>> p.setup_score_players_for_sport('nfl')  # scores and saves the fantasy points for each PlayerStats object
#
#        >>> from roster.classes import Initial
#        >>> initial = Initial()
#        >>> initial.setup('nfl')                    # creates the NFL fantasy roster
#
#
#    3) create a salary "Algorithm Configuration" at http://localhost/admin/salary/salaryconfig/
#
#    4) add a Play Pool at http://localhost/admin/salary/pool/
#
#    5) start celery if its not running (in a terminal, with this command):
#
#        $> celery -A mysite worker -l info
#        $> celery -A mysite beat -S djcelery.schedulers.DatabaseScheduler      # along with worker, allow admin tasks
#        $> celery -A mysite flower                                             # localhost:5555/monitor/
#
#    5) now you can check the checkbox for that Player Pool
#       and select the admin action "Generate Salaries"
#
#    6) create a prize structure
#
#        In [1]: from prize.classes import CashPrizeStructureCreator
#
#        In [2]: creator = CashPrizeStructureCreator()
#
#        In [3]: creator.ad
#        creator.add          creator.added_ranks
#
#        In [3]: creator.add( 1, 1.80 )
#
#        In [4]: create.save()
#        ---------------------------------------------------------------------------
#        NameError                                 Traceback (most recent call last)
#        <ipython-input-4-4c7c22da37e0> in <module>()
#        ----> 1 create.save()
#
#        NameError: name 'create' is not defined
#
#        In [5]: creator.save()
#        <class 'cash.models.CashAmount'>
#
#        In [6]: creator.pr
#        creator.prize_structure        creator.prize_structure_model
#
#        In [6]: creator.prize_structure.buyin = 1
#
#        In [7]: creator.prize_structure.save()
#
#    1) create a contest via the admin panel
#
#    6) create a draftgroup (the draftable players)



#
# Replayer
#   ... in order for the stats replayer to function properly, VM "time syncing"
#       _must_ be disabled. below are commands to list your VM names, and
#       read/modify the time syncing setting via command line.
#
# $> VBoxManage list vms
# $> VBoxManage getextradata dfs_web_1439500760009_74161 VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled
# $> VBoxManage setextradata dfs_web_1439500760009_74161 VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled 1
# $> VBoxManage getextradata dfs_web_1439500760009_74161 VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled
