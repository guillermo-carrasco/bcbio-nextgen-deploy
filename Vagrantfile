# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  # All Vagrant configuration is done here. 

  # We are performing a fresh install of ubuntu 12.04 (precise pangolin)
  config.vm.box = "precise32"

  # Port forwading to 1234 (non standard one) to avoid collision
  config.vm.forward_port 22, 1234

  # Bash provisioning
  config.vm.provision :shell, :path => "shell_provisioner.sh"

end
