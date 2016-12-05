import time

from nerdl.dataset import dataset_splitter_shortener
from nerdl.dataset.cw.cw_dataset_generator import CWDatasetGenerator
from nerdl.dataset.dataset_splitter_shortener import DatasetSplitterShortener
from nerdl.dataset.figer import figer_gold_converter
from settings import path_settings

start = time.time()  # can use time.clock()

################################################################################
# path_settings.CW_CORPUS_FILE
# path_settings.CW_DATASET_CW_TAGS_FILE

# print('>> Generating CW Dataset - CW Tags...')
# cw_ds_gen = CWDatasetGenerator()
# cw_ds_gen.create_dataset(sentence_nb=5000000)
################################################################################
# path_settings.FIGER_GOLD_FILE
# path_settings.FIGER_GOLD_BIO_FILE
# path_settings.FIGER_GOLD_NOT_BIO_FILE

# figer_gold_converter.convert_figer_gold_to_bio()
# figer_gold_converter.convert_figer_gold_to_not_bio()
################################################################################
# dataset_fp = path_settings.CW_DATASET_CW_TAGS_FILE
# train_fp = path_settings.CW_TRAIN_FILE
# test_fp = path_settings.CW_TEST_FILE

# dataset_fp = path_settings.CW_DATASET_CW_TAGS_FILE
# train_fp = path_settings.CW_DATASET_CW_TAGS_FILE.replace('.tsv', '-example.tsv')
# test_fp = path_settings.CW_TEST_FILE.replace('.tsv', '-example.tsv')

dataset_fp = path_settings.FIGER_DATASET_CW_TAGS_FILE
train_fp = path_settings.FIGER_TRAIN_FILE
test_fp = path_settings.FIGER_TEST_FILE

# dataset_fp = path_settings.FIGER_DATASET_FG_TAGS_FILE
# train_fp = path_settings.FIGER_TRAIN_FILE
# test_fp = path_settings.FIGER_TEST_FILE

# dataset_fp = path_settings.FIGER_DATASET_CW_TAGS_FILE
# train_fp = path_settings.FIGER_DATASET_CW_TAGS_FILE.replace('.tsv', '-example.tsv')
# test_fp = path_settings.FIGER_TEST_FILE.replace('.tsv', '-example.tsv')

# dataset_fp = path_settings.FIGER_DATASET_FG_TAGS_FILE
# train_fp = path_settings.FIGER_DATASET_FG_TAGS_FILE.replace('.tsv', '-example.tsv')
# test_fp = path_settings.FIGER_TEST_FILE.replace('.tsv', '-example.tsv')

dss = DatasetSplitterShortener(dataset_fp, train_fp, test_fp)
# dss.split_and_shorten(sentence_nb=1000, print_every=0, min_len=1, max_len=50, test_perc=0)
# dss.split_and_shorten(sentence_nb=2400000, print_every=200000, min_len=1, max_len=50, test_perc=0.2)
dss.split_and_shorten(sentence_nb=0, print_every=200000, min_len=1, max_len=50, test_perc=0)
################################################################################

end = time.time()
print('{} seconds'.format(str(end - start)))
