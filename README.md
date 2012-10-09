## Overview

This is a set of scripts to perform an automatic deployment of the next gen sequencing analysis [pipeline][o1]. You can do it in two ways:
* Perform a local installation of the pipeline in your machine. To do that, a virtual machine is created and the pipeline is installed whithin this virtual machine, then the test suite is run.
* Configure and install the pipeline in [UPPMAX][o5] (see detail below)

[![Build Status](https://secure.travis-ci.org/guillermo-carrasco/bcbio-nextgen-deploy.png?branch=develop)](http://travis-ci.org/guillermo-carrasco/bcbio-nextgen-deploy)

## Local installation

### Required libraries

All the software and dependencies needed by the pipeline are automatically downloaded and installed. However, you need to install the necessary tools for running this script:
* [Vagrant][o2] - To download and install the Virtual Machine
* [Python fabric][o3] - To run the main script

### Running the tests
To run the automatic deployment you just have to type:

            fab -f deploy_on_vm.py deploy

And the script will start installing the pipeline and, when finished, will run the tests.

###Notes
After the installation has finished and the tests have run, you can connect to the VM and take a look at the tests results using the command:

            vagrant ssh

After that, you can turn off the virtual machine with:

            vagrant halt

You can always turn on the virtual machine again with the command:

            vagrant up

For more information about how vagrant works, refear to the [vagrant guide][o4]

## Installation in UPPMAX

### Install

To configure and install the pipeline in UPPMAX you just have to execute the following script:

            python deploy_non_root.py install

This will:
* Set up virtualenvwrapper creating and configurin a proper virtual environment
* Set up the config directory containing the configuration files for the pipeline
* Set up custom modules
* Set up bcbb pipeline code properly
* Download and install SciLifeLab utility scripts
* Run the testsuite

### Remove

To *completely* remove the pipeline and all its configuration execute:
            python setup_uppmax.py purge

####Important note
This will completely remove the directories and configuration files created during the pipeline installation, including virtualenv, and restoring all the configuration files modified during the installation (.bashrc, etc)

[o1]: https://github.com/chapmanb/bcbb/tree/master/nextgen
[o2]: http://vagrantup.com/
[o3]: http://docs.fabfile.org/en/1.4.3/index.html
[o4]: http://vagrantup.com/v1/docs/getting-started/index.html
[o5]: http://www.uppmax.uu.se/
