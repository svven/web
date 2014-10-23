# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "ubuntu/trusty64"

  config.vm.network "forwarded_port", guest: 8000, host: 8080

  config.vm.provision :shell, path: "provision.sh", keep_color: "true", 
	args: "vagrant svven https://dl.dropboxusercontent.com/u/134594/svven/svven_rsa.pub https://dl.dropboxusercontent.com/u/134594/svven/svven_rsa"

  # config.ssh.forward_agent = true

end
