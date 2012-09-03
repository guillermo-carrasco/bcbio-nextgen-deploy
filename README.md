## Overview

This is a set of scripts to perform an automatic deployment of the next gen sequencing analysis [pipeline][o1].


## Installation

### Required libraries

All the software and dependencies needed by the pipeline are automatically downloaded and installed. However, you need to install the necessary tools for running this script:
* [Vagrant][o2] - To download and install the Virtual Machine
* [Python fabric][o3] - To run the main script

## Running the tests
To run the automatic deployment you just have to type:

            fab -f run_testsVM deploy

And the script will start installing the pipeline and, when finished, will run the tests.

###Notes
After the installation has finished and the tests have run, you can connect to the VM and take a look at the tests results using the command:

            vagrant ssh

After that, you can turn off the virtual machine with:

            vagrant halt

You can always turn on the virtual machine again with the command:

            vagrant up

For more information about how vagrant works, refear to the [vagrant guide][o4]

[o1]: https://github.com/chapmanb/bcbb/tree/master/nextgen
[o2]: http://vagrantup.com/
[o3]: http://docs.fabfile.org/en/1.4.3/index.html
[o4]: http://vagrantup.com/v1/docs/getting-started/index.html
