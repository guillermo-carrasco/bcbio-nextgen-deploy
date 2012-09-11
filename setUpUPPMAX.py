#!/usr/bin/python

import os
import shutil
import sys
from subprocess import call
import logging


def install():
    """
    This function installs and set up properly the pipeline in UPPMAX. It performs several steps:
        1.- Install the virtualenvwrapper scripts
        2.- Setup the config repository
        3.- Setup the custom module specifications
        4.- Setup the bcbb pipeline code
        5.- Setup the SciLifeLab utility scripts
        6.- Run the test suite
        7.- Start the bcbb client
    """
    log = logging.getLogger("UPLogger")

    ################################
    # Setting up virtualenvwrapper #
    ################################

    # 1.- Modify .bahrc
    log.info("SETTING UP VIRTUALENVWRAPPER")
    log.info("Editing .bashrc...")
    bashrc = open(os.path.join(os.environ['HOME'], '.bashrc'), 'a')
    f = open('bashLines', 'r')
    for l in f.readlines():
        bashrc.write(l)
    f.close()
    bashrc.close()

    #Add to the current environment the variables added to .bashrc (like doing a source .bashrc)
    os.environ['PATH'] = ':'.join([os.environ['PATH'], os.path.join(os.environ['HOME'], 'opt/mypython/bin')])
    os.environ['PYTHONPATH'] = os.path.join(os.environ['HOME'], 'opt/mypython/lib/python2.6/site-packages')
    # source ~/opt/mypython/bin/virtualenvwrapper.sh ??
    os.environ['WORKON_HOME'] = os.path.join(os.environ['HOME'], '.virtualenvs')

    # 2.- Install virtualenvwrapper
    log.info("Installing virtualenvwrapper...")
    os.makedirs(os.path.join(os.environ['HOME'], 'opt/mypython/lib/python2.6/site-packages'))
    call('easy_install --prefix=~/opt/mypython pip', shell=True)
    call('pip install virtualenvwrapper --install-option=\"--prefix=~/opt/mypython\"', shell=True)

    # 3.- Create a virtual environment "master" for the production pipeline
    log.info("Creating a virtual environment \"master\" for the production pipeline")
    call('. ~/bashrc && \
          module unload python && \
          mkvirtualenv --python=/sw/comp/python/2.7_kalkyl/bin/python master', shell=True)

    # 4.- In order to force the system to use our own python binary instead of
    #     the system's, add the following lines to ~/.virtualenv/postactivate:
    log.info("Editing ~/.virtualenv/postactivate...")
    if not os.path.exists(os.path.join(os.environ['HOME'], '.virtualenv')):
        os.makedirs(os.path.join(os.environ['HOME'], '.virtualenv'))
    p = open(os.path.join(os.environ['HOME'], '.virtualenv/postactivate'), 'a+')
    f = open('virtualenvLines', 'r')
    for l in f.readlines():
        p.write(l)
    f.close()
    p.close()

    ###############################
    # Setting up config directory #
    ###############################


def purge():
    """
    Purge the installation of the pipeline in UPPMAX.
    """
    log = logging.getLogger("UPLogger")

    # Edit the ~/.bashrc configuration file
    log.info('Cleaning .bashrc...')
    b = open(os.path.join(os.environ['HOME'], '.bashrc'), 'r')
    bashrc = b.readlines()
    b.close()
    f = open('bashLines', 'r')
    bashLines = f.readlines()
    f.close()
    b = open(os.path.join(os.environ['HOME'], '.bashrc'), 'w')
    for l in bashrc:
        if l not in bashLines:
            b.write(l)
    b.close()
    
    log.info("Removing created virtualenv...")
    call('. ~/opt/mypython/bin/virtualenvwrapper.sh && \
          rmvirtualenv master', shell=True)

    log.info('Removing opt/* and virtualenvs directories...')
    shutil.rmtree(os.path.join(os.environ['HOME'], 'opt'))
    shutil.rmtree(os.path.join(os.environ['HOME'], '.virtualenv'))
    shutil.rmtree(os.path.join(os.environ['HOME'], '.virtualenvs'))


def test():
    log = logging.getLogger("UPLogger")
    log.info('The test works properly')


if __name__ == '__main__':

    #Parse the funcion
    function_map = {
    'install': install,
    'purge': purge,
    'test': test,
    }

    try:
        function = function_map[sys.argv[1]]
    except KeyError:
        sys.exit('ERROR: Unknown action ' + '\'' + sys.argv[1] + '\'')

    #Prepare the logger (writting to a file and to stdout)
    logger = logging.getLogger("UPLogger")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    h1 = logging.StreamHandler()
    h2 = logging.FileHandler('setUpUPPMAX.log')
    h1.setFormatter(formatter)
    h2.setFormatter(formatter)
    logger.addHandler(h1)
    logger.addHandler(h2)

    #Call the function
    function()
