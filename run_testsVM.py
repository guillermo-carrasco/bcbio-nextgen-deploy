"""
The aim of this script is to perform a deployment of the bcbb-nextgen pipeline into a fresh virtual machine.
It creates a new VM using vagrant and then uses it to pull the full cloudbiolinux (a pipeline requirement) and
the full pipeline, installs them and run the testsuite
"""

import os

#TODO: To execute local commands with fabrit, call them with the function local("command")
#TODO: Error handling with fabric, you can just warn or ask instead of abort...


def clone_biolinux():
    """Function that clones cloudbiolinux from gitHub and installs it on a VM"""


def install_VM():
    """Download, init and up a vagrant VM"""


## Main script
print("Creating testing directory...")
try:
    os.mkdir('testingNextgen')
except OSError, e:
    raise

os.chdir('testingNextgen')
os.mkdir('test2')
