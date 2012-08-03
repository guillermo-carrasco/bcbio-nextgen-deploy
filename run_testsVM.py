"""
The aim of this script is to perform a deployment of the bcbb-nextgen pipeline within a fresh virtual machine.
It creates a new VM using vagrant and then uses it to pull and install the cloudbiolinux requirements and
the full pipeline. Then performs the tests.
"""

from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

#Define the vagrant host
env.hosts = ['vagrant@localhost:2222']


def install_pipeline():
    """Pulls and install the pipeline within the vagrant visrtual machine"""

    run("git clone https://github.com/chapmanb/bcbb.git")
    codedir = '/home/vagrant/bcbb/nextgen'
    with cd(codedir):
        run("sudo python setup.py install")


def install_cloudbiolinux():
    """Function that clones cloudbiolinux from gitHub and installs it on a VM"""

    local("git clone https://github.com/chapmanb/cloudbiolinux.git")
    local("fab -f cloudbiolinux/fabfile.py -H vagrant -c cloudbiolinux/contrib/minimal/fabricrc_debian.txt install_biolinux:packagelist=cloudbiolinux/contrib/minimal/main.yaml,target=packages")


def install_VM():
    """Download, init, provide and up a vagrant VM able to run the pipeline"""

    #Error handling, just in case that already exists a vagrant box with the same name
    with settings(warn_only=True):
        result = local("vagrant box add debian_squeeze_32 http://mathie-vagrant-boxes.s3.amazonaws.com/debian_squeeze_32.box", capture=True)
    if result.failed and not confirm("It looks like already exists a vagrant box with this name in your system, do you want to continue using this box? (y/n)"):
        abort("Aborting at user request")
    local("vagrant up")


## Main method
def deploy():
    print("Prepare and init the Virtual Machine...")
    install_VM()
    print("DONE")
    print("Preparing dependencies...")
    install_cloudbiolinux()
    print("DONE")
    print("Installing the pipeline...")
    install_pipeline()
    print("DONE")
