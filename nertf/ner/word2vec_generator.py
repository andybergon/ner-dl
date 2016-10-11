import gensim
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for line in open(self.dirname):
            yield line.split()


def generate_word2vec(sentences_filepath, word2vec_filepath, word2vec_txt_filepath=None):
    sentences = MySentences(sentences_filepath)  # memory-friendly iterator

    model = gensim.models.Word2Vec(sentences, min_count=1, iter=10, size=300, window=5, workers=4)

    model.save(word2vec_filepath)

    if word2vec_txt_filepath is not None:
        model.save_word2vec_format(word2vec_txt_filepath, binary=False)
