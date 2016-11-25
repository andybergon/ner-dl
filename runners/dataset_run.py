import time

from nerdl.dataset.cw.cw_dataset_generator import CWDatasetGenerator

start = time.time()  # can use time.clock()

################################################################################
# path_settings.CW_CORPUS_FILE
# path_settings.CW_DATASET_CW_TAGS_FILE

print('>> Generating CW Dataset - CW Tags...')
cw_ds_gen = CWDatasetGenerator()
cw_ds_gen.create_dataset(sentence_nb=100000)
################################################################################

# max_sentence_len = settings.MAX_SENTENCE_LEN

# k_sentences = 10
# path_settings.WORD2VEC_TXT_FILE = path_settings.CW_W2V_TXT_FILE.replace('.txt', '-old.txt')
# path_settings.TRAINING_FILE = path_settings.TRAINING_FILE.replace('training.tsv', 'training_{}k.tsv'.format(k_sentences))
# path_settings.TEST_FILE = path_settings.TEST_FILE.replace('test.tsv', 'test_{}k.tsv'.format(k_sentences))


# print('>> Generating Training/Test...')
# start_partial = time.time()
# tagger = FigerTagger()
# ttg = TestTrainingGenerator(tagger)
# ttg.create_training_and_test(
#                              sentence_nb=10000,
#                              skip_sentences_longer_than=max_sentence_len,
#                              test_percentage=0)
# end_partial = time.time()
# print('<< Generated Training/Test in {} seconds.\n'.format(str(end_partial - start_partial)))

################################################################################
# dataset_fp = path_settings.FIGER_DATASET_FG_TAGS_FILE
# train_fp = path_settings.FIGER_TRAIN_FILE
# test_fp = path_settings.FIGER_TEST_FILE

# dataset_splitter.split_dataset(dataset_fp, train_fp, test_fp)
################################################################################

end = time.time()
print('{} seconds'.format(str(end - start)))
