import logging

import gensim

from nerdl.ner.utils import tokenizer
from settings import path_settings
from settings import settings

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class Word2VecGenerator(object):
    def __init__(self, filepath, use_tokenizer=True):
        self.filepath = filepath
        self.use_tokenizer = use_tokenizer

    def __iter__(self):
        for line in open(self.filepath):
            if self.use_tokenizer:
                yield tokenizer.tokenize_in_words(line)
            else:
                yield line.split()  # faster but not accurate


def generate_word2vec(use_tokenizer=True, also_pickle_save=False):
    sentences_filepath = path_settings.SENTENCES_FILE
    word2vec_filepath = path_settings.WORD2VEC_FILE
    word2vec_txt_filepath = path_settings.WORD2VEC_TXT_FILE

    min_count = settings.W2V_MIN_COUNT
    iter = settings.W2V_ITER
    size = settings.W2V_SIZE
    window = settings.W2V_WINDOW
    workers = settings.W2V_WORKERS

    sentences = Word2VecGenerator(sentences_filepath, use_tokenizer)  # memory-friendly iterator
    model = gensim.models.Word2Vec(sentences=sentences,
                                   min_count=min_count,
                                   iter=iter,
                                   size=size,
                                   window=window,
                                   workers=workers)

    model.save_word2vec_format(word2vec_txt_filepath)
    if also_pickle_save:
        model.save(word2vec_filepath)  # pickle-save
