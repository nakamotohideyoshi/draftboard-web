# DFS

[![Codeship Status for runitoncedevs/dfs](https://codeship.com/projects/c31f7a20-ae27-0132-eb40-0283b9bcbbf1/status?branch=master)](https://codeship.com/projects/68807)

<!--

NOTE: Pulled from 'readme' file, not sure if this is accurate.


The purpose of this project is to make it insanely easy to start up a python3.4 + django1.7 project. It uses Vagrant to do so.

##### Prerequisites:

* [Vagrant](https://www.vagrantup.com/downloads.html)
* Git 		

##### Step 1:

1. git <code>clone https://GITUSERNAME@bitbucket.org/GITUSERNAME/vagrant-django.git</code>
2.	 cd vagrant-django
3. 	 vagrant up
4. 	 vagrant ssh
  
To connect from a browser on your local computer, bring up gunicorn or runserver:

    cd /vagrant && ./manage.py runserver 127.0.0.1:8000

or

    cd /vagrant && /home/vagrant/venv/bin/gunicorn mysite.wsgi 
-->

##Client-Side Development


### Requirements

To build the front-end project you'll need to install the following.

* [Node](https://nodejs.org/)
* [Node Version Manager (nvm)](https://github.com/creationix/nvm)


### Setup

    
In the project root, install all global dependiencies. 

    $ npm run install_global_modules

Install local prject dependencies.

    $ npm install


### Building
    
Install and activate the node version the project uses (dictated by the .nvrmc file)

    $ nvm install
    $ nvm use


In the package.json file, you'll see our npm tasks under the "scripts" key. These are what we'll use to run Webpack's devserver, test, and build the app.

Run the tasks with npm's run command:

    $ npm run <task name>


### Testing

We're using Mocha, the testing options are defined in <code>/static/src/js/test/mocha.opts</code>

To run the tests:

    $ npm run test
