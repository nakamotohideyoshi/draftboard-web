#!/usr/bin/env bash
sudo -u vagrant /home/vagrant/venv/bin/python /vagrant/manage.py makemigrations
sudo -u vagrant /home/vagrant/venv/bin/python /vagrant/manage.py migrate
sudo -u vagrant /home/vagrant/venv/bin/python /vagrant/manage.py loaddata /vagrant/site-setup/initial_data.json
