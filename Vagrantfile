# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  # All Vagrant configuration is done here. 

  # We are performing a fresh install of ubuntu 12.04 (precise pangolin)
  config.vm.box = "precise32"

  config.vm.provision :chef_solo do |chef|
    # This path will be expanded relative to the project directory
    chef.cookbooks_path = "cookbooks"
    # Install the basic libraries to be able to pull the pipeline and install it within the virtual machine
    chef.add_recipe("apt")
    chef.add_recipe("git")
    chef.add_recipe("python")
  end
end
