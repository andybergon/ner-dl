import os
import gensim
import logging

import settings


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sentences_file = os.path.join(settings.DATA_ROOT, 'replaced', 'cw_1_sentences_10k.tsv')
w2v_file = os.path.join(settings.WORD2VEC_ROOT, 'w2v')
w2v_txt_file = os.path.join(settings.WORD2VEC_ROOT, 'w2v.txt')


class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for line in open(self.dirname):
            yield line.split()


sentences = MySentences(sentences_file)  # memory-friendly iterator

model = gensim.models.Word2Vec(sentences, min_count=1, iter=10, size=300, window=5, workers=4)

model.save(w2v_file)
model.save_word2vec_format(w2v_txt_file, binary=False)
