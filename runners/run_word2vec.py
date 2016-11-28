import os
import time

from nerdl.ner.w2v import word2vec_generator
from settings import path_settings

start = time.time()

################################################################################
# path_settings.SENTENCES_FILE
# path_settings.WORD2VEC_TXT_FILE
# path_settings.WORD2VEC_FILE

path_settings.SENTENCES_FILE = path_settings.CW_SENTENCES_FILE
path_settings.WORD2VEC_TXT_FILE = path_settings.CW_W2V_TXT_FILE

print('>> Generating Word2Vec vectors...')
word2vec_generator.generate_word2vec(use_tokenizer=True)
################################################################################

end = time.time()
print('<< Word2Vec vectors generated in {} seconds'.format(str(end - start)))

