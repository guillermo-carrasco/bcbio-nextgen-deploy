{
    "postactivate": [
        "# We don't want UPPMAX's custom python", 
        "PATH=\"${PATH/'/sw/comp/python/2.6.6_kalkyl/bin'}\"", 
        "# We unset PYTHONHOME set by the module system,", 
        "# otherwise the system will not use the python", 
        "# of virtualenv", 
        "unset PYTHONHOME", 
        "# Make the modules load after activating a virtual environment", 
        "source ~/opt/config/modules"
    ], 
    ".bashrc": [
        "# User specific aliases and functions", 
        "#Set up python and virtualenvenvironmen", 
        "export PATH=$PATH:~/opt/mypython/bin", 
        "export PYTHONPATH=~/opt/mypython/lib/python2.6/site-packages:~/opt", 
        "source ~/opt/mypython/bin/virtualenvwrapper.sh", 
        "export WORKON_HOME=~/.virtualenvs", 
        "export MODULEPATH=${MODULEPATH}:~/opt/modules", 
        "#Set up umask so created files/directories are read/writeable by group", 
        "umask 007", 
        "#Set up python DRMAA module", 
        "export DRMAA_LIBRARY_PATH=/bubo/home/h5/roman/dev/slurm-drmaa/trunk/slurm_drmaa/.libs/libdrmaa.so", 
        "export DRMAA_PATH=$DRMAA_LIBRARY_PATH"
    ]
}