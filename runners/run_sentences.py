import os
import time

from nerdl.dataset.sentences_extractor import SentencesExtractor
from nerdl.ner.w2v import word2vec_generator
from settings import path_settings

start = time.time()

################################################################################
# dataset_fp
# sentences_fp

dataset_fp = path_settings.CW_DATASET_CW_TAGS_FILE
sentences_fp = path_settings.CW_SENTENCES_FILE

print('>> Extracting sentences from dataset...')
se = SentencesExtractor()
se.extract_sentences(dataset_fp, sentences_fp)
################################################################################

end = time.time()
print('<< Sentences extracted in {} seconds'.format(str(end - start)))

