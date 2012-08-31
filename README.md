## Overview

This is a set of scripts to perform an automatic deployment of the next gen sequencing analysis [pipeline][o1].


## Installation

### Required libraries

Most of the software and dependencies needed by the pipeline are automatically downloaded. However, you need to install the following dependencies:
* [Vagrant][o2] - To download and install the Virtual Machine
* [Python fabric][o3] - To run the main script

## Running the tests
To run the automatic deployment you just have to type:

            fab -f run_testsVM deploy


[o1]: https://github.com/chapmanb/bcbb/tree/master/nextgen
[o2]: http://vagrantup.com/
[o3]: http://docs.fabfile.org/en/1.4.3/index.html