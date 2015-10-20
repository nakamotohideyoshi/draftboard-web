#!/usr/bin/env bash

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
sudo echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get update
### apt-get install -y mongodb-org   ### install latest.   the speficic version install is on the next line
sudo apt-get install -y mongodb-org=3.0.2 mongodb-org-server=3.0.2 mongodb-org-mongos=3.0.2 mongodb-org-tools=3.0.2
sudo apt-get install mongodb-org-shell