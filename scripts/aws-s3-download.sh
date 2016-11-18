#!/bin/bash
# set -x;

aws s3 cp cw_1_sentences.tsv.tar.gz s3://ner-dl/

aws s3 cp mid_name_types.tsv.tar.gz s3://ner-dl/

aws s3 cp w2v.txt.tar.gz s3://ner-dl/

aws s3 cp training.tar.gz s3://ner-dl/
aws s3 cp test.tar.gz s3://ner-dl/
