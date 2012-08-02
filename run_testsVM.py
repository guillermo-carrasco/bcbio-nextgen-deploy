"""
The aim of this script is to perform a deployment of the bcbb-nextgen pipeline within a fresh virtual machine.
It creates a new VM using vagrant and then uses it to pull and install the cloudbiolinux requirements and
the full pipeline. Then performs the tests.
"""

from fabric.api import local


def install_cloudbiolinux():
    """Function that clones cloudbiolinux from gitHub and installs it on a VM"""

    local("git clone https://github.com/chapmanb/cloudbiolinux.git")
    local("fab -f cloudbiolinux/fabfile.py -H vagrant -c cloudbiolinux/contrib/minimal/fabricrc_debian.txt install_biolinux:packagelist=cloudbiolinux/contrib/minimal/main.yaml,target=packages")


def install_VM():
    """Download, init, provide and up a vagrant VM able to run the pipeline"""

    local("vagrant box add debian_squeeze_32 http://mathie-vagrant-boxes.s3.amazonaws.com/debian_squeeze_32.box")
    local("vagrant up")


## Main script
print("Prepare and init the Virtual Machine...")
install_VM()
print("DONE")
print("Preparing dependencies...")
install_cloudbiolinux()
print("DONE")
