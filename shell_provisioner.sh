#!/bin/sh

##########################################################################################################
# Script to provide the Vagrant VM with all the necessary deps to run the tests and isntall the pipeline #
##########################################################################################################

set -e # Exit script immediately on first error.

# Install python-software-properties and add necessary repositories
apt-get update
apt-get install -y python-software-properties
add-apt-repository -y ppa:scilifelab/scilifelab
add-apt-repository -y ppa:debian-med/ppa

#Update the system and install dependencies
wget http://dl.dropbox.com/u/3046000/mosaik32.tar.gz && tar xvzf mosaik32.tar.gz && sudo cp mosaik/* /usr/local/bin
apt-get update
apt-get install -y snpeff picard-tools bwa bowtie bowtie2 freebayes fastqc-0.10.1 gatk r-base texlive texlive-latex-extra tophat openjdk-6-jre samtools unzip lftp cufflinks wigtools python-pip python-dev python-setuptools python-nose git
pip install numpy

#Install snpEff database
lftp -e 'pget -n 8 http://downloads.sourceforge.net/project/snpeff/databases/v3_0/snpEff_v3_0_GRCh37.63.zip; quit'
unzip snpEff_v3_0_GRCh37.63.zip -d /usr/share/snpEff/ && rm snpEff_v3_0_GRCh37.63.zip
