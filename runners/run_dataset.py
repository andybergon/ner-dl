import time

from nerdl.dataset import dataset_splitter_shortener
from nerdl.dataset.cw.cw_dataset_generator import CWDatasetGenerator
from nerdl.dataset.dataset_splitter_shortener import DatasetSplitterShortener
from nerdl.dataset.figer import figer_gold_converter

start = time.time()  # can use time.clock()

################################################################################
# path_settings.CW_CORPUS_FILE
# path_settings.CW_DATASET_CW_TAGS_FILE

# print('>> Generating CW Dataset - CW Tags...')
cw_ds_gen = CWDatasetGenerator()
cw_ds_gen.create_dataset(sentence_nb=5000000)
################################################################################
# path_settings.FIGER_GOLD_FILE
# path_settings.FIGER_GOLD_BIO_FILE
# path_settings.FIGER_GOLD_NOT_BIO_FILE

# figer_gold_converter.convert_figer_gold_to_bio()
# figer_gold_converter.convert_figer_gold_to_not_bio()
################################################################################

# max_sentence_len = settings.MAX_SENTENCE_LEN

# k_sentences = 10
# path_settings.WORD2VEC_TXT_FILE = path_settings.CW_W2V_TXT_FILE.replace('.txt', '-old.txt')
# path_settings.TRAINING_FILE = path_settings.TRAINING_FILE.replace('training.tsv', 'training_{}k.tsv'.format(k_sentences))
# path_settings.TEST_FILE = path_settings.TEST_FILE.replace('test.tsv', 'test_{}k.tsv'.format(k_sentences))

# tagger = FigerTagger()
# ttg = TestTrainingGenerator(tagger)
# ttg.create_training_and_test(
#                              sentence_nb=10000,
#                              skip_sentences_longer_than=max_sentence_len,
#                              test_percentage=0)

################################################################################
# dataset_fp = path_settings.FIGER_DATASET_FG_TAGS_FILE
# train_fp = path_settings.FIGER_TRAIN_FILE
# test_fp = path_settings.FIGER_TEST_FILE

# dss = DatasetSplitterShortener(dataset_fp, train_fp, test_fp)
# dss.split_and_shorten()
################################################################################

end = time.time()
print('{} seconds'.format(str(end - start)))
