#!/usr/bin/env bash

#
# this script is primarily used by vagrant, so MAKING migrations should never be useful,
# because they should already exist
#sudo -u vagrant /home/vagrant/venv/bin/python /vagrant/manage.py makemigrations

#
# the migrations should exist to be able to do this.
# 'migrate' is the new 'syncdb' (since django 1.7)
sudo -u vagrant /home/vagrant/venv/bin/python /vagrant/manage.py migrate

#
# deprecated
#sudo -u vagrant /home/vagrant/venv/bin/python /vagrant/manage.py loaddata /vagrant/site-setup/initial_data.json
