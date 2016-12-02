#!/bin/bash
# set -x;

# $1 == folder name
compress() {
    echo "Compressing $1.tar.gz"
    tar -czvf $1.tar.gz ../data/$1
}

# $1 == compressed filename
upload() {
    echo "Uploading $1.tar.gz"
    aws s3 cp $1.tar.gz s3://ner-dl/
}

# $1 == compressed filename
remove_targz() {
    echo "Removing $1.tar.gz"
    rm $1.tar.gz
}

compress_upload_remove() {
    compress $1
    upload $1
    remove_targz $1
}

compress_upload_remove dataset
compress_upload_remove mid
compress_upload_remove word2vec
