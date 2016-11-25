#!/bin/bash
# set -x;

sudo yum update -y
sudo yum install git
git clone https://github.com/andybergon/ner-dl.git

ner-dl/scripts/convert-settings-examples.sh
ner-dl/scripts/aws-s3-download.sh

wget https://repo.continuum.io/archive/Anaconda2-4.2.0-Linux-x86_64.sh
bash Anaconda2-4.2.0-Linux-x86_64.sh -b -p $HOME/anaconda2
# source ~/.bashrc # if manual and yes at export
export PATH=$HOME/anaconda2/bin:$PATH

conda upgrade --all

conda install nltk
ner-dl/scripts/nltk_download.py

conda install scipy numpy wheel pandas matplotlib scikit-learn gensim pickle -y # All requested packages already installed.

conda install -c conda-forge tensorflow -y # 0.10.0 # 0.11.0rc2
conda install -c conda-forge theano -y # 0.8.2
# conda install -c conda-forge keras -y # 1.0.7 # version too old
conda install -c CCXD keras -y # 1.1.1

# pip search keras # 1.1.1
# pip install keras

mkdir $HOME/.keras
cp ner-dl/scripts/keras.json $HOME/.keras/keras.json # get from git folder

# data/ from s3
