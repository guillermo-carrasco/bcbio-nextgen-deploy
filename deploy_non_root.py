#!/usr/bin/python

import os
import shutil
import sys
import logging
import json
import subprocess
from os.path import join as pjoin
from subprocess import check_call


def install(env, config_lines):
    """
    Installs and set up properly the bcbio-nextgen pipeline in UPPMAX.
    """

    log = logging.getLogger("UPLogger")
    #Common dirs
    home = env['HOME']
    deploy_dir = os.getcwd()
    opt_dir = pjoin(home, 'opt')
    inHPC = env.has_key('module')
    if inHPC:
        modules_dir = pjoin(home, 'opt/modules')
    config_dir = pjoin(home, 'opt/config')
    bcbb_dir = pjoin(home, 'opt/bcbb')

    ################################
    # Setting up virtualenvwrapper #
    ################################

    #Modify .bahrc
    log.info("SETTING UP VIRTUALENVWRAPPER")
    log.info("Editing .bashrc...")
    bashrc = open(pjoin(home, '.bashrc'), 'a')
    if inHPC:
        bash_lines = config_lines['.bashrc_HPC']
    else:
        bash_lines = config_lines['.bashrc_non_root']
    for l in config_lines['.bashrc_HPC']:
        bashrc.write(l+'\n')
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
    python_dir = pjoin(home, 'opt/mypython/lib/python2.6/site-packages')
    if not os.path.exists(python_dir):
        os.makedirs(python_dir)
    check_call(install_and_create_virtualenv, shell=True, env=env)

    #Modify ~/.virtualenvs/postactivate...
    log.info("Editing ~/.virtualenvs/postactivate...")
    p = open(pjoin(home, '.virtualenvs/postactivate'), 'a')
    for l in config_lines['postactivate']:
        p.write(l+'\n')
    p.close()
    #Create ~/.modules file
    shutil.copy(pjoin(deploy_dir, 'modules'), pjoin(home, '.modules'))


    #############################
    # Setting up custom modules #
    #############################
    log.info("SETTING UP CUSTOM MODULES")
    os.chdir(opt_dir)
    if os.path.exists(modules_dir):
        shutil.rmtree(modules_dir)
    check_call('git clone http://github.com/SciLifeLab/modules.sf.net.git modules', shell=True, env=env)
    os.chdir(modules_dir)
    check_call('git checkout master', shell=True, env=env)
    
    #################################
    # Setting up bcbb pipeline code #
    #################################
    log.info("SETTING UP BCBB PIPELINE CODE")
    log.info("Downloading pipeline code and checking out master branches...")
    os.chdir(opt_dir)
    if os.path.exists(bcbb_dir):
        shutil.rmtree(bcbb_dir)
    check_call('git clone --recursive http://github.com/SciLifeLab/bcbb.git bcbb', shell=True, env=env)
    check_call('cd bcbb && git checkout master && cd nextgen/bcbio/scilifelab && git checkout master', shell=True, env=env)

    log.info("Installing the pipeline...")
    install_code_in_production = """
        . ~/.bashrc &&
        cd ~/opt/bcbb/nextgen &&
        workon master &&
        pip install numpy &&
        python setup.py install
        """
    check_call(install_code_in_production, shell=True, env=env)
    
    ##########################################
    # Setting up scilifelab utility scriipts #
    ##########################################
    log.info("SETTING UP SCILIFELAB UTILITY SCRIPTS")
    log.info("Downloading and installing scilifelab scripts...")
    if os.path.exists('scilifelab'):
        shutil.rmtree('scilifelab')
    download_and_install_scripts = """
        git clone http://github.com/SciLifeLab/scilifelab.git scilifelab &&
        cd scilifelab && git checkout master &&
        . ~/.bashrc &&
        workon master &&
        python setup.py install
        """
    check_call(download_and_install_scripts, shell=True, env=env)

    ######################
    # Running test suite #
    ######################
    log.info("RUNNING TEST SUITE")
    log.info("Preparing testsuite...")
    os.chdir(pjoin(bcbb_dir, 'nextgen/tests/data/automated'))
    shutil.copy(pjoin(deploy_dir, 'post_process.yaml'), 'post_process.yaml')
    
    # Run the testsuite with reduced test data
    run_tests = """
        . ~/.bashrc &&
        workon master &&
        python ~/opt/bcbb/nextgen/tests/runtests_drmaa.py
        """
    log.info("Running test suite...")
    check_call(run_tests, shell=True, env=env)


def purge(env, config_lines):
    """
    Purge the installation of the pipeline in UPPMAX.
    """
    home = env['HOME']
    opt_dir = pjoin(home, 'opt')
    log = logging.getLogger("UPLogger")

    # Edit the ~/.bashrc configuration file
    log.info('Cleaning .bashrc...')
    b = open(pjoin(home, '.bashrc'), 'r')
    bashrc = b.readlines()
    b.close()
    bash_lines = config_lines['.bashrc_HPC']
    b = open(pjoin(home, '.bashrc'), 'w')
    for l in bashrc:
        if l.rstrip() not in bash_lines:
            b.write(l)
    b.close()
    
    log.info("Removing created virtualenv...")
    try:
        check_call('. ~/opt/mypython/bin/virtualenvwrapper.sh && \
                    rmvirtualenv master', shell=True, env=env)
    except subprocess.CalledProcessError:
        log.warning('No master virtualenv found, just skipping this step!')
        pass

    try:
        os.remove(pjoin(home, '.modules'))
    except OSError:
        pass

    if os.path.exists(pjoin(home, '.virtualenvs/postactivate')):
        log.info("Cleaning .virtualenvs/postactivate...")
        p = open(pjoin(home, '.virtualenvs/postactivate'), 'r')
        postactive = p.readlines()
        p.close()
        virtualenvLines = config_lines['postactivate']
        p = open(pjoin(home, '.virtualenvs/postactivate'), 'w')
        for l in postactive:
            if l.rstrip() not in virtualenvLines:
                p.write(l)
        p.close()

    if os.path.exists(opt_dir):
        log.info('Removing ~/opt directory...')
        shutil.rmtree(opt_dir)


if __name__ == '__main__':

    #Work with a copy of the current environment and tune it
    env = dict(os.environ)
    env['PATH'] = ':'.join([env['PATH'], pjoin(env['HOME'], 'opt/mypython/bin')])
    env['PYTHONPATH'] = pjoin(env['HOME'], 'opt/mypython/lib/python2.6/site-packages')

    #Parse the funcion
    function_map = {
        'install': install,
        'purge': purge,
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
    h2 = logging.FileHandler('setup_uppmax.log')
    h1.setFormatter(formatter)
    h2.setFormatter(formatter)
    logger.addHandler(h1)
    logger.addHandler(h2)

    #Config json file
    try:
        f = open('env.json', 'r')
    except IOError:
        print "ERROR: Could not find env.json file."
        print "Try to do a \"git pull origin master\" to restore the file."
        raise

    config_lines = json.load(f)
    f.close()

    #check_call the function
    function(env, config_lines)
