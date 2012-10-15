#!/usr/bin/python

import os
import shutil
import sys
import logging
import json
import subprocess
import platform
from os.path import join as pjoin
from subprocess import check_call
from subprocess import Popen


def _setUp(function):
    """
    Set up the environment to correctly install the pipeline depending on where the script
    is executed. Also set up te log handler. 
    """
    #Work with a copy of the current environment and tune it
    env = dict(os.environ)
    env['PATH'] = ':'.join([env['PATH'], pjoin(env['HOME'], 'opt/mypython/bin')])
    #Detect python version and set the proper PYTHONPATH
    version = '.'.join(platform.python_version_tuple()[0:2])
    env['PYTHONPATH'] = pjoin(env['HOME'], 'opt/mypython/lib/python{version}/site-packages').format(version=version)

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
    function(env, config_lines)


def _install(env, config_lines):
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
    bcbb_dir = pjoin(home, 'opt/bcbb')

    #Bash commands
    install_and_create_virtualenv ='''
        easy_install --prefix=~/opt/mypython pip &&
        pip install virtualenvwrapper --install-option="--prefix=~/opt/mypython" &&
        . ~/.bashrc &&
        {module_unload_python}
        mkvirtualenv --python={python_bin} master
        '''

    install_code_in_production = """
        . ~/.bashrc &&
        cd ~/opt/bcbb/nextgen &&
        workon master &&
        pip install numpy &&
        python setup.py install
        """

    download_and_install_scripts = """
        git clone http://github.com/SciLifeLab/scilifelab.git scilifelab &&
        cd scilifelab && git checkout master &&
        . ~/.bashrc &&
        workon master &&
        python setup.py install
        """

    run_tests = """
        . ~/.bashrc &&
        workon master &&
        {runtests}
        """
    #Format the commands depending on the execution environment
    if inHPC: 
        install_and_create_virtualenv = install_and_create_virtualenv.format(module_unload_python='module unload python &&', python_bin='/sw/comp/python/2.7_kalkyl/bin/python')
        bash_lines = config_lines['.bashrc_HPC']
        postactivate_lines = config_lines['postactivate_HPC']
        run_tests = run_tests.format(runtests='python ~/opt/bcbb/nextgen/tests/runtests_drmaa.py')
    else:
        install_and_create_virtualenv = install_and_create_virtualenv.format(module_unload_python='', python_bin='/usr/bin/python')
        bash_lines = config_lines['.bashrc_non_root']
        postactivate_lines = config_lines['postactivate_non_root']
        run_tests = run_tests.format(runtests='nosetests -s -v --with-xunit -a standard')

    ##########################
    # Setting up virtualenvwrapper #
    ##########################

    #Modify .bahrc
    log.info("SETTING UP VIRTUALENVWRAPPER")
    log.info("Editing .bashrc...")
    
    #Removing non-interactive checking (otherwise we cannot source configuration files)
    sed_command = '''sed '/[ -z "$PS1" ] && return/d' < ~/.bashrc > ~/.bashrc_'''
    check_call(sed_command, shell=True)
    shutil.move(pjoin(home, '.bashrc_'), pjoin(home, '.bashrc'))
    
    bashrc = open(pjoin(home, '.bashrc'), 'a')
    for l in bash_lines:
        try:
            l = l.format(pythonpath=env['PYTHONPATH'])
        except KeyError:
            pass
        bashrc.write(l+'\n')
    bashrc.close()

    ###################################

    log.info("Installing virtualenvwrapper and creating a virtual environment \"master\" for the production pipeline...")
    python_dir = env['PYTHONPATH']
    if not os.path.exists(python_dir):
        os.makedirs(python_dir)
    Popen(install_and_create_virtualenv, shell=True, executable='/bin/bash', env=env).wait()

    #Modify ~/.virtualenvs/postactivate...
    log.info("Editing ~/.virtualenvs/postactivate...")
    p = open(pjoin(home, '.virtualenvs/postactivate'), 'a')
    for l in postactivate_lines:
        p.write(l+'\n')
    p.close()
    #Create ~/.modules file
    shutil.copy(pjoin(deploy_dir, 'modules'), pjoin(home, '.modules'))


    if inHPC:
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
    check_call('git clone --recursive http://github.com/guillermo-carrasco/bcbb.git bcbb', shell=True, env=env)
    check_call('cd bcbb && git checkout master && cd nextgen/bcbio/scilifelab && git checkout master', shell=True, env=env)

    log.info("Installing the pipeline...")
    Popen(install_code_in_production, shell=True, executable='/bin/bash', env=env).wait()
    
    ##########################################
    # Setting up scilifelab utility scriipts #
    ##########################################
    log.info("SETTING UP SCILIFELAB UTILITY SCRIPTS")
    log.info("Downloading and installing scilifelab scripts...")
    if os.path.exists('scilifelab'):
        shutil.rmtree('scilifelab')
    Popen(download_and_install_scripts, shell=True, executable='/bin/bash', env=env).wait()

    ######################
    # Running test suite #
    ######################
    log.info("RUNNING TEST SUITE")
    log.info("Preparing testsuite...")
    os.chdir(pjoin(bcbb_dir, 'nextgen/tests/data/automated'))
    shutil.copy(pjoin(deploy_dir, 'post_process.yaml'), 'post_process.yaml')
    
    # Run the testsuite with reduced test data (if not in Travis-CI)
    if not env.has_key('TRAVIS'):
        log.info("Running test suite...")
        os.chdir(pjoin(bcbb_dir, 'nextgen/tests'))
        Popen(run_tests, shell=True, executable='/bin/bash', env=env).wait()


def _uninstall(env, config_lines):
    """
    Remove the installation of the pipeline in UPPMAX.
    """
    home = env['HOME']
    inHPC = env.has_key('module')
    opt_dir = pjoin(home, 'opt')        
    bcbb_dir = pjoin(opt_dir, 'bcbb')
    scilife_dir = pjoin(opt_dir, 'scilifelab')
    modules_dir = ''
    log = logging.getLogger("UPLogger")

    if inHPC:
        bash_lines = config_lines['.bashrc_HPC']
        postactivate_lines = config_lines['postactivate_HPC']
        modules_dir = pjoin(opt_dir, 'modules')
    else:
        bash_lines = config_lines['.bashrc_non_root']
        postactivate_lines = config_lines['postactivate_non_root']

    # Edit the ~/.bashrc configuration file
    for i in range(len(bash_lines)):
        try:
            bash_lines[i] = bash_lines[i].format(pythonpath=env['PYTHONPATH'])
        except KeyError:
            pass
    
    log.info('Cleaning .bashrc...')
    b = open(pjoin(home, '.bashrc'), 'r')
    bashrc = b.readlines()
    b.close()
    
    b = open(pjoin(home, '.bashrc'), 'w')
    for l in bashrc:
        if l.rstrip() not in bash_lines:
            b.write(l)
    b.close()
    
    log.info("Removing created virtualenv...")
    rmvirtualenv_failed = Popen('. ~/opt/mypython/bin/virtualenvwrapper.sh && \
                                                      rmvirtualenv master', shell=True, executable='/bin/bash', env=env).wait()
    if rmvirtualenv_failed:
        log.warning('No master virtualenv found, just skipping this step!')
        
    try:
        os.remove(pjoin(home, '.modules'))
    except OSError:
        pass

    if os.path.exists(pjoin(home, '.virtualenvs/postactivate')):
        log.info("Cleaning .virtualenvs/postactivate...")
        p = open(pjoin(home, '.virtualenvs/postactivate'), 'r')
        postactive = p.readlines()
        p.close()
        virtualenvLines = postactivate_lines
        p = open(pjoin(home, '.virtualenvs/postactivate'), 'w')
        for l in postactive:
            if l.rstrip() not in virtualenvLines:
                p.write(l)
        p.close()

    if os.path.exists(bcbb_dir):
        log.info('Removing ~/opt/bcbb directory...')
        shutil.rmtree(bcbb_dir)

    if os.path.exists(modules_dir):
        log.info('Removing ~/opt/modules directory...')
        shutil.rmtree(modules_dir)

    if os.path.exists(scilife_dir):
        log.info('Removing ~/opt/scilifelab directory...')
        shutil.rmtree(scilife_dir)


if __name__ == '__main__':

    #Parse the funcion
    function_map = {
        'install': _install,
        'uninstall': _uninstall,
    }

    try:
        function = function_map[sys.argv[1]]
    except KeyError:
        sys.exit('ERROR: Unknown action ' + '\'' + sys.argv[1] + '\'')

    #check_call the function
    _setUp(function)
