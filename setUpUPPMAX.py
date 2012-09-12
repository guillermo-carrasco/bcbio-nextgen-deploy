#!/usr/bin/python

import os
from os.path import join as pjoin
import shutil
import sys
from subprocess import call
import logging


def install(env):
    """
    Installs and set up properly the pipeline in UPPMAX creating a virtualenv.
    """

    log = logging.getLogger("UPLogger")

    ################################
    # Setting up virtualenvwrapper #
    ################################

    #Modify .bahrc
    log.info("SETTING UP VIRTUALENVWRAPPER")
    log.info("Editing .bashrc...")
    bashrc = open(pjoin(env['HOME'], '.bashrc'), 'a')
    f = open('bashLines', 'r')
    for l in f.readlines():
        bashrc.write(l)
    f.close()
    bashrc.close()


    #Install virtualenvwrapper and create a virtual environment "master" for the production pipeline
    install_and_create_virtualenv ='''
        easy_install --prefix=~/opt/mypython pip &&
        pip install virtualenvwrapper --install-option="--prefix=~/opt/mypython" &&
        . ~/.bashrc &&
        module unload python &&
        mkvirtualenv --python=/sw/comp/python/2.7_kalkyl/bin/python master
        '''

    log.info("Installing virtualenvwrapper and creating a virtual environment \"master\" for the production pipeline...")
    os.makedirs(pjoin(env['HOME'], 'opt/mypython/lib/python2.6/site-packages'))
    call(install_and_create_virtualenv, shell=True, env=env)

    #Modify ~/.virtualenvs/postactivate...
    log.info("Editing ~/.virtualenvs/postactivate...")
    p = open(pjoin(env['HOME'], '.virtualenvs/postactivate'), 'a')
    f = open('virtualenvLines', 'r')
    for l in f.readlines():
        p.write(l)
    f.close()
    p.close()

    ###############################
    # Setting up config directory #
    ###############################


def purge(env):
    """
    Purge the installation of the pipeline in UPPMAX.
    """
    log = logging.getLogger("UPLogger")

    # Edit the ~/.bashrc configuration file
    log.info('Cleaning .bashrc...')
    b = open(pjoin(env['HOME'], '.bashrc'), 'r')
    bashrc = b.readlines()
    b.close()
    f = open('bashLines', 'r')
    bashLines = f.readlines()
    f.close()
    b = open(pjoin(env['HOME'], '.bashrc'), 'w')
    for l in bashrc:
        if l not in bashLines:
            b.write(l)
    b.close()
    
    log.info("Removing created virtualenv...")
    call('. ~/opt/mypython/bin/virtualenvwrapper.sh && \
          rmvirtualenv master', shell=True, env=env)

    log.info('Removing ~/opt and virtualenvs directories...')
    shutil.rmtree(pjoin(env['HOME'], 'opt'))
    shutil.rmtree(pjoin(env['HOME'], '.virtualenvs'))


def test(env):
    log = logging.getLogger("UPLogger")
    log.info('The test works properly')


if __name__ == '__main__':

    #Work with a copy of the current environment and tune it
    env = dict(os.environ)
    env['PATH'] = ':'.join([env['PATH'], pjoin(env['HOME'], 'opt/mypython/bin')])
    env['PYTHONPATH'] = pjoin(env['HOME'], 'opt/mypython/lib/python2.6/site-packages')

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
    function(env)
