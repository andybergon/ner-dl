import os
import time

from nerdl.ner.w2v import word2vec_generator
from settings import path_settings

start = time.time()
print('>> Generating word2vec vectors...')

# path_settings.REPLACED_CORPUS_FILE
# path_settings.WORD2VEC_TXT_FILE
# path_settings.WORD2VEC_FILE

path_settings.REPLACED_CORPUS_FILE = path_settings.REPLACED_CORPUS_FILE.replace('.tsv', '_1000k.tsv')
path_settings.WORD2VEC_TXT_FILE = path_settings.CW_W2V_TXT_FILE

word2vec_generator.generate_word2vec(use_tokenizer=True)

end = time.time()
print('<< Word2vec vectors generated in {} seconds'.format(str(end - start)))

