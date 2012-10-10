#!/usr/bin/python

"""
The aim of this script is to perform a deployment of the bcbb-nextgen pipeline within a fresh virtual machine.
It creates a new VM using vagrant and then uses it to pull and install the pipeline and its requirements.
Then performs the tests.
"""

from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.operations import sudo
import os

#Define the vagrant host
env.hosts = ['vagrant@127.0.0.1:1234']
env.user = 'vagrant'
env.password = 'vagrant'
codedir = '/home/vagrant/bcbio-nextgen-deploy'

def _install_pipeline():
    """Pulls and install the pipeline within the vagrant virtual machine"""

    run("git clone https://github.com/guillermo-carrasco/bcbio-nextgen-deploy.git")
    with cd(codedir):
        run("python deploy_non_root.py install")


def _install_VM():
    """Download, init, provide and up a vagrant VM able to run the pipeline"""

    #Error handling, just in case that already exists a vagrant box with the same name
    with settings(warn_only=True):
        result = local("vagrant box add precise32 http://files.vagrantup.com/precise32.box", capture=True)
    if result.failed and not confirm("It looks like already exists a vagrant box with the name \"precise32\" on your system, do you want to continue using this box? (y/n)"):
        abort("Aborting at user request")
    local("vagrant up")


def _provision_VM():
    """Install necessary software to run the pipeline in the virtual machine"""
    #Add repositories
    sudo('apt-get update')
    sudo('apt-get install -y python-software-properties')
    sudo('add-apt-repository -y ppa:scilifelab/scilifelab')
    sudo('add-apt-repository -y ppa:debian-med/ppa')
    sudo('apt-get update')
    #Install pipeline dependencies
    sudo('apt-get install -y snpeff-2 picard-tools bwa bowtie bowtie2 \
              freebayes fastqc-0.10.1 gatk r-base texlive texlive-latex-extra \
              tophat openjdk-6-jre samtools unzip lftp cufflinks wigtools \
              python-pip python-dev python-setuptools python-nose \
              python-yaml git')
    run('lftp -e \'pget -n 8 http://downloads.sourceforge.net/project/snpeff/databases/v2_0_5/snpEff_v2_0_5_GRCh37.63.zip; quit\'')
    sudo('unzip snpEff_v2_0_5_GRCh37.63.zip -d /usr/share/snpEff/ && rm snpEff_v2_0_5_GRCh37.63.zip')


## Main method
def install():
    print("Installing the Virtual Machine...")
    _install_VM()
    print("DONE")
    print("Provisioning Virtual Machine with software dependencies...")
    _provision_VM()
    print("Installing the pipeline and running the testsuite...")
    _install_pipeline()
    print("DONE")
