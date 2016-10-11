import numpy as np

from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.core import Dropout
from keras.layers.wrappers import Bidirectional
from keras.layers.wrappers import TimeDistributed
from keras.models import Sequential
from keras.models import load_model
from keras.regularizers import l2

np.random.seed(0)  # for debugging


class NERModel:
    def __init__(self, reader):

        self.reader = reader
        self.model = None

        self.all_X, self.all_Y = reader.get_data()

        self.train_X = None
        self.test_X = None
        self.train_Y = None
        self.test_Y = None

    def load(self, filepath):
        self.model = load_model(filepath)

    def save(self, filepath):
        self.model.save(filepath)

    def print_summary(self):
        print(self.model.summary())

    def train(self, test_split=0.2, epochs=20, batch=50, dropout=0.2, reg_alpha=0.0, units=150, layers=1):

        test_split_mask = np.random.rand(len(self.all_X)) < (1 - test_split)

        self.train_X = self.all_X[test_split_mask]
        self.train_Y = self.all_Y[test_split_mask]
        self.test_X = self.all_X[~test_split_mask]
        self.test_Y = self.all_Y[~test_split_mask]
        print(self.train_X.shape)
        print(self.train_Y.shape)

        # TODO: use 'self.reader' variables
        input_shape = self.all_X.shape[1:3]  # (max_length, w2v_length), e.g. (95,300)
        output_dim = self.all_Y.shape[2]

        self.model = Sequential()

        self.model.add(Bidirectional(LSTM(units,
                                          return_sequences=True,
                                          W_regularizer=l2(reg_alpha),
                                          U_regularizer=l2(reg_alpha),
                                          b_regularizer=l2(reg_alpha)),
                                     input_shape=input_shape))

        self.model.add(Dropout(dropout))

        if layers > 1:
            self.model.add(Bidirectional(LSTM(units,
                                              return_sequences=True,
                                              W_regularizer=l2(reg_alpha),
                                              U_regularizer=l2(reg_alpha),
                                              b_regularizer=l2(reg_alpha))))

            self.model.add(Dropout(dropout))

        self.model.add(TimeDistributed(Dense(output_dim, activation='softmax',
                                             W_regularizer=l2(reg_alpha),
                                             b_regularizer=l2(reg_alpha))))

        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        print(self.model.summary())

        # actual training
        self.model.fit(self.train_X, self.train_Y, nb_epoch=epochs, batch_size=batch)

    def evaluate(self):
        scores = self.model.evaluate(self.test_X, self.test_Y, verbose=0)
        print("Accuracy: %.2f%%" % (scores[1] * 100))

    def predict_sentence(self, sentence, pad=False):

        # Look up the embeddings for the words
        sentence = sentence[:self.reader.max_sentence_len + 1]  # TODO: check if correct position
        X = self.reader.encode_sentence(sentence)

        # Predict the labels
        predictions = self.model.predict(X, batch_size=1)

        # Lookup the tags given the class embeddings
        tags = self.reader.decode_prediction_sequence(predictions[0])

        if not pad:
            tags = tags[-len(sentence):]

        tag_str = ''
        for t in tags:
            tag_str += t + ' '

        return tags
