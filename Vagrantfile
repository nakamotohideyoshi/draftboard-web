# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

Vagrant.configure(2) do |config|

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.

  #
  # configure the dev box - we're calling it "web"
  config.vm.define "web" do |web|

    #
    # specify the base vm - you will need to
    # make sure VT-x / SVM is enabled in the BIOS for 64 bit VMs (usually it is)
    web.vm.box = "ubuntu/trusty64"

    #
    # forward http port to the box
    web.vm.network "forwarded_port", host: 8888, guest: 80

    #
    # lets use 'bootstrap.sh' for provisioning
    web.vm.provision :shell, path: "./site-setup/bootstrap.sh"

    #
    # start the vm in GUI mode which can lead us to witness
    # better error messages from virtualbox than vagrant gives
    config.vm.provider "virtualbox" do |v|
        v.gui = true
    end

  end

end
