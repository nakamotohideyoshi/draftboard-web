# -*- mode: ruby -*-
# vi: set ft=ruby :

# NOTE: if on Yosemite and up, you may need to fix http://gielberkers.com/fixing-vagrant-port-forwarding-osx-yosemite/

Vagrant.configure(2) do |config|

  #
  # configure a webserver
  config.vm.define "web" do |web|
    #
    # specify the base vm
    web.vm.box = "ubuntu/trusty64"

    #
    # forward http traffic from port 8080 to port 8000 on the vm
    web.vm.network "forwarded_port", host: 5555, guest: 5555
    # Map local IP 192.168.66.6 to the VM.
    web.vm.network :private_network, ip: "192.168.66.6"
    #
    # lets use 'bootstrap.sh' for provisioning
    web.vm.provision :shell, path: "./site-setup/bootstrap.sh"

    #
    # launch the vm in "gui" mode which can
    # help alert us to errors which vagrant
    # simply cant let us know about via cmd line
    config.vm.provider "virtualbox" do |v|
        v.gui = false

        #
        # Note: non-default settings and/or giving
        #   too much memory/cores to the VM
        #   can really hammer your computers performance!
        #
        # should drastically help performance,
        # but remove if anything stops working
        v.memory = 4096
        v.cpus = 3

    end

  end

end
