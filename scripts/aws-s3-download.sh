#!/bin/bash
# set -x;

# $1 == filename, $2 == data/<location>
function download() {
    aws s3 cp s3://ner-dl/$1.tar.gz ./$1.tar.gz
    mkdir ../data/$2 # if already exists just prints it
    tar -xvf $1.tar.gz -C ../data/$2 # error if no space left on device
    rm $1.tar.gz
}

download cw-dataset dataset/cw-dataset # TODO: all datasets
download word2vec
download mid_name_types.tsv mid
# download cw_1_sentences.tsv ??
