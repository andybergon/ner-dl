#!/bin/bash
# set -x;

aws s3 cp s3://ner-dl/cw_1_sentences.tsv.tar.gz ./cw_1_sentences.tsv.tar.gz
tar -xvf cw_1_sentences.tsv.tar.gz -C ../data/sentences
rm cw_1_sentences.tsv.tar.gz

aws s3 cp s3://ner-dl/mid_name_types.tsv.tar.gz ./mid_name_types.tsv.tar.gz
tar -xvf mid_name_types.tsv.tar.gz -C ../data/mid
rm mid_name_types.tsv.tar.gz

aws s3 cp s3://ner-dl/w2v.txt.tar.gz ./w2v.txt.tar.gz
tar -xvf w2v.txt.tar.gz -C ../data/word2vec
rm w2v.txt.tar.gz

aws s3 cp s3://ner-dl/training.tar.gz ./training.tar.gz
tar -xvf training.tar.gz -C ../data/training
rm training.tar.gz

aws s3 cp s3://ner-dl/test.tar.gz ./test.tar.gz
tar -xvf test.tar.gz -C ../data/test
rm test.tar.gz
