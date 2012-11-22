## Overview

This is a set of scripts to perform an automatic deployment of the next gen sequencing analysis [pipeline][o1]. You can do it in two ways:
* Configure and install the pipeline in [UPPMAX][o5] (see detail below)
* Perform a local installation of the pipeline within a virtual machine.
* Install the pipeline locally in your machine

Current build status: [![Build Status](https://secure.travis-ci.org/guillermo-carrasco/bcbio-nextgen-deploy.png?branch=master)](http://travis-ci.org/guillermo-carrasco/bcbio-nextgen-deploy)

## Installation in UPPMAX

### Requirements
To use this script you need python 2.7 or higher. In UPPMAX you can just do a:

        module load python/2.7

to get python 2.7.

### Install

To configure and install the pipeline in UPPMAX you just have to execute the following command (after cloning this repository):

            python deploy_non_root.py install

This will:
* Set up virtualenvwrapper creating and configuring a proper virtual environment
* Set up the config directory containing the configuration files for the pipeline
* Set up custom modules with correct software versions
* Set up bcbb pipeline code properly
* Download and install SciLifeLab utility scripts
* Run the testsuite in background:
    * This will run a job that will write the tests results in ~/opt/bcbb/nextgen/tests/tests_results.out
    * You'll find also an XML file with a summary of the test results in ~/opt/bcbb/nextgen/tests/nosetests.xml

You can also install a specific version of the pipeline using the -v option. To do so, you just have to specify a commit sha
when running the installation script, like this:

        python deploy_non_root.py -v 1116 install

And the script will checkout for this commit before installing.

#### Notes
If you don't want to run the test suite after the installation, you can specify this:

    python deploy_non_root.py --no-tests install


### Uninstall

To *completely* uninstall the pipeline and all its configuration files/directories execute:
            python deploy_non_root.py uninstall


## Local installation within a virtual machine

### Requirements

All the software and dependencies needed by the pipeline are automatically downloaded and installed. However, you need to install the necessary tools for running this script:
* [Vagrant][o2] - To download and install the Virtual Machine
* [Python fabric][o3] - To run the main script

Furthermore, in order to correctly execute all the tests, please *have in mind that 2GB of memory are reserved for the Virtual Machine when it's on*.

### Installing the pipeline and running the tests
To install the virtual machine, the pipeline within it and run the tests, just type:

            fab -f deploy_on_vm.py install

And the script will start installing the virtual machine and the pipeline. When the installation is finished, the tests will run.

### Installing in several virtual machines
If you have a cluster of __vagrant__ virtual machines configured in [host-only networking][o6] mode, you can install the pipeline in all of them just specifying the "comma separated" list of IPs:

    fab -f deploy_on_vm.py -H 10.10.10.3,10.10.10.4 install

This will install the pipeline and run the tests in all of the specified machines.

###Notes
#### For the multi-VM installation
* It is necessary that the virtual machines specified in the list are Vagrant VMs, or at least, they need to have a user _vagrant_ (with password also _vagrant_), as the fabric calls are executed with this user.
* If you're using your own machines (not creating a new one with the script), please take into account that the script has been tested and prepared for Ubuntu 12.04, other operating systems are not officially supported.

#### About Vagrant in general
After the installation has finished and the tests have run, you can connect to the VM and take a look at the tests results using the command:

            vagrant ssh

After that, you can turn off the virtual machine with:

            vagrant halt

You can always turn on the virtual machine again with the command:

            vagrant up

So you'll have a Virtual Machine whith the pipeline installed to test it whenever you want without installing any software in your system but vagrant and fabric.

For more information about how vagrant works, refear to the [vagrant guide][o4]

## Local installation

To install the pipeline in your machine, execute the command:
            python deploy_non_root.py install

*NOTE*: The installation of the pipeline itself doesn't need root permissions, but in this case, you have to take care of the installation of all the software dependencies of the pipeline. Read the [pipeline documentation][o1] for more information about what software do you need.

## Important note about the uninstall function

This will completely remove the directories and configuration files created during the pipeline installation, including master virtualenv with all python dependencies installed, and restoring all the configuration files modified during the installation (.bashrc, etc)

[o1]: https://github.com/scilifelab/bcbb/tree/master/nextgen
[o2]: http://vagrantup.com/
[o3]: http://docs.fabfile.org/en/1.4.3/index.html
[o4]: http://vagrantup.com/v1/docs/getting-started/index.html
[o5]: http://www.uppmax.uu.se/
[o6]: http://vagrantup.com/v1/docs/host_only_networking.html
