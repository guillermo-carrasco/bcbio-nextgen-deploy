"""
The aim of this script is to perform a deployment of the bcbb-nextgen pipeline within a fresh virtual machine.
It creates a new VM using vagrant and then uses it to pull and install the cloudbiolinux requirements and
the full pipeline. Then performs the tests.
"""

import os

#TODO: To execute local commands with fabrit, call them with the function local("command")
#TODO: Error handling with fabric, you can just warn or ask instead of abort...


def install_cloudbiolinux():
    """Function that clones cloudbiolinux from gitHub and installs it on a VM"""


def install_VM():
    """Download, init, provide and up a vagrant VM"""


## Main script
print("Creating testing directory...")
try:
    os.mkdir('testingNextgen')
except OSError, e:
    raise

os.chdir('testingNextgen')
