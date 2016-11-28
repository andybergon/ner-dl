import os
import time
import datetime

from settings import path_settings
from settings import settings

start = time.time()

################################################################################
# settings.TAG2VEC_CLASS_LIST

k_sentences = 1000
max_sentence_len = settings.MAX_SENTENCE_LEN

path_settings.WORD2VEC_TXT_FILE = path_settings.CW_W2V_TXT_FILE.replace('.txt', '-old.txt')
path_settings.TRAINING_FILE = path_settings.TRAINING_FILE.replace('training.tsv', 'training_{}k.tsv'.format(k_sentences))
path_settings.TEST_FILE = path_settings.TEST_FILE.replace('test.tsv', 'test_{}k.tsv'.format(k_sentences))

# path_settings.WORD2VEC_TXT_FILE = path_settings.FIGER_W2V_TXT_FILE
# path_settings.TRAINING_FILE = path_settings.FIGER_TRAIN_FILE
# path_settings.TEST_FILE = path_settings.FIGER_TEST_FILE

dt = datetime.datetime.now().isoformat()
path_settings.MODEL_FILE = path_settings.MODEL_FILE.replace('.h5', '_{}.h5'.format(dt))

path_settings.TRAINING_CHECKPOINT_FILE = path_settings.TRAINING_FILE.replace('.tsv', '-checkpoint.tsv')

# model = KerasNERModel()
# model.train()
# REMEMBER TO CLEAN 'TRAINING_CHECKPOINT_FILE'
# model.resume_train()
################################################################################

end = time.time()
print('{} seconds'.format(str(end - start)))
