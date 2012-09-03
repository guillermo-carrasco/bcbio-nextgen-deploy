#!/usr/bin/python

"""
The aim of this script is to perform a deployment of the bcbb-nextgen pipeline within a fresh virtual machine.
It creates a new VM using vagrant and then uses it to pull and install the cloudbiolinux requirements and
the full pipeline. Then performs the tests.
"""

from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
import os

#Define the vagrant host
env.hosts = ['vagrant@localhost:1234']
env.user = 'vagrant'
env.password = 'vagrant'
codedir = '/home/vagrant/bcbb_chapmanb/nextgen'

def install_pipeline():
    """Pulls and install the pipeline within the vagrant visrtual machine"""

    run("git clone https://github.com/guillermo-carrasco/bcbb_chapmanb.git")
    with cd(codedir):
        run("sudo python setup.py install")


def install_VM():
    """Download, init, provide and up a vagrant VM able to run the pipeline"""

    #Error handling, just in case that already exists a vagrant box with the same name
    with settings(warn_only=True):
        result = local("vagrant box add precise32 http://files.vagrantup.com/precise32.box", capture=True)
    if result.failed and not confirm("It looks like already exists a vagrant box with this name in your system, do you want to continue using this box? (y/n)"):
        abort("Aborting at user request")
    local("vagrant up")


## Main method
def deploy():
    print("Prepare and init the Virtual Machine...")
    install_VM()
    print("DONE")
    print("Installing the pipeline...")
    install_pipeline()
    print("DONE")
    print("Running tests")
    with cd(os.path.join(codedir, 'tests')):
    	run("nosetests -s -v")
    run("DONE")
