# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "phusion/ubuntu-14.04-amd64"

  config.vm.network "forwarded_port", guest: 8000, host: 8880

  config.vm.provision :shell, path: "bootstrap.sh"

  config.vm.provision :shell, :path => 'bootstrap-user.sh', :privileged => false

  config.ssh.forward_agent = true  

end
