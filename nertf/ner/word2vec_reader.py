import numpy as np
import pandas as pd
from keras.preprocessing import sequence


class Word2VecReader:
    def __init__(self, word2vec_filepath=None, max_sentence_len=80, n_tag_classes=6):

        self.wordvecs = None
        self.word_to_ix_map = {}

        self.n_features = 0
        self.n_tag_classes = n_tag_classes
        self.max_sentence_len = max_sentence_len

        self.n_sentences_all = 0
        self.tag_vector_map = {}

        if word2vec_filepath:
            self.read_word2vec(word2vec_filepath)

    def read_word2vec(self, word2vec_filepath):
        print('Loading Word2Vec...')

        # skiprows=1 to skip first line
        self.wordvecs = pd.read_table(word2vec_filepath, sep=' ', header=None, skiprows=1)
        # <class 'pandas.core.frame.DataFrame'>
        # print(self.wordvecs.shape)

        self.word_to_ix_map = {}
        for ix, row in self.wordvecs.iterrows():
            self.word_to_ix_map[row[0]] = ix

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
            if word in self.word_to_ix_map:
                X.append(self.wordvecs[self.word_to_ix_map[word]])
            elif skip_unknown_words:
                continue
            else:
                new_wv = 2 * np.random.randn(self.n_features) - 1  # sample from normal distribution
                norm_const = np.linalg.norm(new_wv)
                new_wv /= norm_const
                X.append(new_wv)

        outer_X.append(X)

        return sequence.pad_sequences(outer_X, maxlen=self.max_sentence_len, dtype=np.float64)

    def decode_prediction_sequence(self, pred_seq):
        pred_tags = []

        for class_prs in pred_seq:
            class_vec = np.zeros(self.n_tag_classes, dtype=np.int32)
            class_vec[np.argmax(class_prs)] = 1

            if tuple(class_vec.tolist()) in self.tag_vector_map:
                pred_tags.append(self.tag_vector_map[tuple(class_vec.tolist())])

        return pred_tags
