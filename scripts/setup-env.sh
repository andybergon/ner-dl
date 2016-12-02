#!/bin/bash
# set -x;

wget https://repo.continuum.io/archive/Anaconda2-4.2.0-Linux-x86_64.sh
bash Anaconda2-4.2.0-Linux-x86_64.sh -b -p $HOME/anaconda2 # -b -p == auto-yes
# source ~/.bashrc # if manual and yes at export
export PATH=$HOME/anaconda2/bin:$PATH

conda upgrade --all -y

conda create -n py27 python=2.7 anaconda
conda create -n py35 python=3.5 anaconda

source activate py27

# use part of aws-setup.sh
