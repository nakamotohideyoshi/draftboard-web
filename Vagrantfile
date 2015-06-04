# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  #
  # configure a webserver
  config.vm.define "web" do |web|
    #
    # specify the base vm
    web.vm.box = "ubuntu/trusty64"

    #
    # forward http traffic to port 8888 on the vm
    web.vm.network "forwarded_port", host: 8888, guest: 80

    #
    # lets use 'bootstrap.sh' for provisioning
    web.vm.provision :shell, path: "./site-setup/bootstrap.sh"

    #
    # launch the vm in "gui" mode which can
    # help alert us to errors which vagrant
    # simply cant let us know about via cmd line
    config.vm.provider "virtualbox" do |v|
        v.gui = true

        #
        # should drastically help performance,
        # but remove if anything stops working
        v.memory = 1024
        v.cpus = 1

    end

  end

end
