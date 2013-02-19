# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  # All Vagrant configuration is done here. 

  # We are performing a fresh install of ubuntu 12.04 (precise pangolin)
  config.vm.box = "precise64"

  #Needed at least 2GB of memory (requirement of picard-tools)
  config.vm.customize ["modifyvm", :id, "--memory", 2048]

  # Port forwading to 1234 (non standard one) to avoid collision
  config.vm.forward_port 22, 1234

end
