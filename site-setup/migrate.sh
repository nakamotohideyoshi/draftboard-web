#!/usr/bin/env bash

#
# the migrations should exist to be able to do this.
# 'migrate' is the new 'syncdb' (since django 1.7)
sudo -u vagrant /home/vagrant/venv/bin/python /vagrant/manage.py migrate
