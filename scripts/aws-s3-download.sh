#!/bin/bash
# set -x;

# $1 == filename, $2 == data/<location>
download() {
    echo "Downloading from S3: $1.tar.gz in ../data/$2"
    aws s3 cp s3://ner-dl/$1.tar.gz ./$1.tar.gz
    mkdir -p ../data/$2 # if already exists just prints it
    tar -xvf $1.tar.gz -C ../data/$2 # error if no space left on device
    rm $1.tar.gz
}

download cw-dataset dataset
download mid_name_types.tsv mid
# download dataset # TODO: all datasets
# download mid
download word2vec

# download cw
