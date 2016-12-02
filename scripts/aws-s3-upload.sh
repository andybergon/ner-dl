#!/bin/bash
# set -x;

aws s3 cp cw_1_sentences.tsv.tar.gz s3://ner-dl/

aws s3 cp mid_name_types.tsv.tar.gz s3://ner-dl/

aws s3 cp w2v.txt.tar.gz s3://ner-dl/

aws s3 cp training.tar.gz s3://ner-dl/
aws s3 cp test.tar.gz s3://ner-dl/

# gets folder
function compress() {
    tar ../data/$1 $1
}

# gets compressed file
function upload() {
    aws s3 cp $1.tar.gz s3://ner-dl/
}

function compress_and_upload(){
    compress $1
    upload $1
}

compress_and_upload dataset
compress_and_upload mid
