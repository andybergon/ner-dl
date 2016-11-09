import numpy as np
import pandas as pd
from keras.preprocessing import sequence

import path_settings
import settings


class Word2VecReader:
    def __init__(self):
        self.word2vec_txt_filepath = path_settings.WORD2VEC_TXT_FILE
        self.max_sentence_len = settings.MAX_SENTENCE_LEN

        self.wordvecs = None
        self.word2vec_map = {}
        self.n_features = 0

        if self.word2vec_txt_filepath:
            self.load_word2vec()

    def load_word2vec(self):
        print('Loading Word2Vec...')

        # skiprows=1 to skip first line
        self.wordvecs = pd.read_table(self.word2vec_txt_filepath, sep=' ', header=None, skiprows=1)
        # <class 'pandas.core.frame.DataFrame'>
        # print(self.wordvecs.shape)

        for ix, row in self.wordvecs.iterrows():
            self.word2vec_map[row[0]] = ix

        print('Word2Vec loaded.')

        # axis=1 for columns
        self.wordvecs = self.wordvecs.drop(self.wordvecs.columns[0], axis=1).as_matrix()
        # <type 'numpy.ndarray'>
        print('Word2Vec shape: {}'.format(self.wordvecs.shape))

        self.n_features = len(self.wordvecs[0])
        # print(self.n_features)

    def encode_sentence(self, sentence, skip_unknown_words=False):
        X = []
        outer_X = []

        for word in sentence:
            if skip_unknown_words:
                continue
            else:
                encoded_word = self.encode_word(word)
                X.append(encoded_word)

        outer_X.append(X)

        return sequence.pad_sequences(outer_X, maxlen=self.max_sentence_len, dtype=np.float64)

    def encode_word(self, word):
        if word in self.word2vec_map:
            encoded_wv = self.wordvecs[self.word2vec_map[word]]
        else:
            encoded_wv = 2 * np.random.randn(self.n_features) - 1  # sample from normal distribution
            norm_const = np.linalg.norm(encoded_wv)
            encoded_wv /= norm_const

            # TODO: check if needed and correct, add unknown words
            # self.word2vec_map[word] = self.wordvecs.shape[0]
            # self.wordvecs = np.vstack((self.wordvecs, encoded_wv))

        return encoded_wv
