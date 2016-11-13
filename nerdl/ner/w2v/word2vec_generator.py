import logging

import gensim

from nerdl.ner.utils import tokenizer
from settings import path_settings
from settings import settings

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class Word2VecGenerator(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for line in open(self.dirname):
            yield tokenizer.tokenize_sentence(line)
            # yield line.split()  # faster but not accurate


def generate_word2vec():
    sentences_filepath = path_settings.REPLACED_CORPUS_FILE
    word2vec_filepath = path_settings.WORD2VEC_FILE
    word2vec_txt_filepath = path_settings.WORD2VEC_TXT_FILE

    min_count = settings.W2V_MIN_COUNT
    iter = settings.W2V_ITER
    size = settings.W2V_SIZE
    window = settings.W2V_WINDOW
    workers = settings.W2V_WORKERS

    sentences = Word2VecGenerator(sentences_filepath)  # memory-friendly iterator
    model = gensim.models.Word2Vec(sentences, min_count, iter, size, window, workers)

    model.save(word2vec_filepath)
    model.save_word2vec_format(word2vec_txt_filepath, binary=False)
