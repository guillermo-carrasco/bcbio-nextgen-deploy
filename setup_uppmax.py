#!/usr/bin/python

import os
from os.path import join as pjoin
import shutil
import sys
from subprocess import check_call
import logging


def install(env):
    """
    Installs and set up properly the bcbio-nextgen pipeline in UPPMAX.
    """

    log = logging.getLogger("UPLogger")
    #Common dirs
    opt_dir = pjoin(env['HOME'], 'opt')
    modules_dir = pjoin(env['HOME'], 'opt/modules')
    config_dir = pjoin(env['HOME'], 'opt/config')
    bcbb_dir = pjoin(env['HOME'], 'opt/bcbb')

    ################################
    # Setting up virtualenvwrapper #
    ################################

    #Modify .bahrc
    log.info("SETTING UP VIRTUALENVWRAPPER")
    log.info("Editing .bashrc...")
    bashrc = open(pjoin(env['HOME'], '.bashrc'), 'a')
    f = open('bash_lines', 'r')
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
    check_call(install_and_create_virtualenv, shell=True, env=env)

    #Modify ~/.virtualenvs/postactivate...
    log.info("Editing ~/.virtualenvs/postactivate...")
    p = open(pjoin(env['HOME'], '.virtualenvs/postactivate'), 'a')
    f = open('virtualenv_lines', 'r')
    for l in f.readlines():
        p.write(l)
    f.close()
    p.close()

    ###############################
    # Setting up config directory #
    ###############################
    log.info("SETTING UP CONFIG REPOSITORY")
    if os.path.exists(config_dir):
        shutil.rmtree(config_dir)
    os.chdir(opt_dir)
    log.info("Cloning config repository...")
    check_call('git clone git@code.scilifelab.se:bcbb_config config', shell=True, env=env)
    os.chmod('config', 0700)
    log.info("Checking out biologin production branch...")
    os.chdir('config')
    check_call('git checkout biologin', shell=True, env=env)
    log.info("Creating symlink to Galaxy\'s tool-data directory...")
    os.symlink('/bubo/nobackup/uppnex/reference/biodata/galaxy/tool-data', 'tool-data')
    log.info("Generate SHA digest and update...")
    check_call('git rev-parse --short --verify HEAD > ~/.config_version', shell=True, env=env)

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
    os.symlink(pjoin(config_dir, 'tests/data/automated/post_process.yaml'), 'post_process.yaml')
    run_tests = """
        . ~/.bashrc &&
        workon master &&
        sbatch ~/opt/scilifelab/batch/nosetests_run.sh
        """
    log.info("Running test suite...")
    check_call(run_tests, shell=True, env=env)


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
    f = open('bash_lines', 'r')
    bash_lines = f.readlines()
    f.close()
    b = open(pjoin(env['HOME'], '.bashrc'), 'w')
    for l in bashrc:
        if l not in bash_lines:
            b.write(l)
    b.close()
    
    log.info("Removing created virtualenv...")
    check_call('. ~/opt/mypython/bin/virtualenvwrapper.sh && \
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
    h2 = logging.FileHandler('setup_uppmax.log')
    h1.setFormatter(formatter)
    h2.setFormatter(formatter)
    logger.addHandler(h1)
    logger.addHandler(h2)

    #check_call the function
    function(env)
