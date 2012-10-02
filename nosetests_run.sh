#!/bin/bash
#SBATCH -p devel
#SBATCH -N 1
#SBATCH -J bcbb_testsuite
#SBATCH -A a2010002
#SBATCH -D .
#SBATCH --mail-user=user@scilifelab.se
#SBATCH --mail-type=ALL
#SBATCH -o nosetest_job.out
#SBATCH -e nosetest_job.err

nosetests -v -s --with-xunit -a standard $1
