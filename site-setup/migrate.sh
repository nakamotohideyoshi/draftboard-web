#!/usr/bin/env bash

#
# the migrations should exist to be able to do this.
sudo -u vagrant /home/vagrant/venv/bin/python3 manage.py migrate --settings mysite.settings.local


