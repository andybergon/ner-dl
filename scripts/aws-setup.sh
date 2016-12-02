#!/bin/bash
# set -x;

# sudo yum update -y
# sudo yum install git -y
# git clone https://github.com/andybergon/ner-dl.git

echo RUN FROM 'scripts' FOLDER!
echo RUN AS '. ./aws-setup.sh' OR 'source ./aws-setup.sh' TO MAKE EXPORT COMMANDS WORK
# cd $HOME/ner-dl/scripts; . ./aws-setup.sh

echo 'Please, copy ".aws" folder manually'
# sudo apt-get install awscli # depends on AMI
./aws-s3-download.sh

cp ../settings/settings.py.example ../settings/settings.py
cp ../settings/net_settings.py.example ../settings/net_settings.py
mkdir ../data/model/ # check

wget https://repo.continuum.io/archive/Anaconda2-4.2.0-Linux-x86_64.sh
bash Anaconda2-4.2.0-Linux-x86_64.sh -b -p $HOME/anaconda2 # -b -p == auto-yes
rm Anaconda2-4.2.0-Linux-x86_64.sh
# source ~/.bashrc # if manual and yes at export
export PATH=$HOME/anaconda2/bin:$PATH

conda upgrade --all -y

conda install nltk -y # All requested packages already installed.
./nltk_download.py

conda install scipy numpy wheel pandas matplotlib scikit-learn -y # All requested packages already installed.
conda install gensim -y
# pickle already installed

conda install -c conda-forge tensorflow -y # 0.10.0 # 0.11.0rc2
conda install -c conda-forge theano -y # 0.8.2
# conda install -c conda-forge keras -y # 1.0.7 # version too old
conda install -c CCXD keras -y # 1.1.1

# anaconda search keras
# OR
# pip search keras # 1.1.1
# pip install keras

mkdir -p $HOME/.keras
cp ./keras.json $HOME/.keras/keras.json

export PYTHONPATH=$HOME/ner-dl
