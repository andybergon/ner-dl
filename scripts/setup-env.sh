#!/bin/bash
# set -x;

# install anaconda

conda upgrade --all

conda create -n py27 python=2.7 anaconda
conda create -n py35 python=3.5 anaconda

source activate py27

conda install nltk -n py27


# tensorflow
conda install -c conda-forge tensorflow -n py27 # 0.10.0

# theano
conda install -c conda-forge theano -n py27

# keras
conda install -c conda-forge keras -n py27 # 1.0.7
