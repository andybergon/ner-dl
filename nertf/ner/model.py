import cPickle as pickle

import numpy as np
from keras.layers import Dense  # TODO: slow. necessary to load on import?
from keras.layers import LSTM
from keras.layers.core import Dropout
from keras.layers.wrappers import Bidirectional
from keras.layers.wrappers import TimeDistributed
from keras.models import Sequential
from keras.models import load_model
from keras.regularizers import l2

import tokenizer

np.random.seed(0)  # for debugging


class NERModel:
    def __init__(self, reader=None, generator=None):

        self.w2v_reader = reader
        self.batch_generator = generator

        self.model = None

    def print_summary(self):
        print(self.model.summary())

    def compile(self, dropout=0.2, reg_alpha=0.0, units=128, layers=1):

        # (max_length, w2v_length), e.g. (95,300)
        input_shape = (self.batch_generator.max_sentence_len, self.w2v_reader.n_features)
        # e.g. (6)
        output_dim = self.batch_generator.nb_classes
        print('Input Shape: {}'.format(input_shape))
        print('Output Dimension: {}'.format(output_dim))

        self.model = Sequential()

        self.model.add(Bidirectional(LSTM(units,
                                          return_sequences=True,
                                          W_regularizer=l2(reg_alpha),
                                          U_regularizer=l2(reg_alpha),
                                          b_regularizer=l2(reg_alpha)),
                                     input_shape=input_shape))

        self.model.add(Dropout(dropout))

        # TODO: manage more than 2 layers
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

    def train_on_batches(self, nb_epoch, batch_size, save_every_x_batches=1):
        nb_batch = 0

        for epoch in range(nb_epoch):
            print('epoch {}'.format(epoch))
            for X_batch, Y_batch in self.batch_generator.generate_training_batch():
                self.model.fit(X_batch, Y_batch, batch_size=batch_size, nb_epoch=1)
                nb_batch += 1
                if nb_batch % save_every_x_batches == 0:
                    self.save_model()

    def train_on_generator(self, samples_per_epoch, nb_epoch, max_q_size, nb_worker, pickle_safe):
        generator = self.batch_generator.generate_training_batch()
        self.model.fit_generator(generator, samples_per_epoch=samples_per_epoch, nb_epoch=nb_epoch,
                                 max_q_size=max_q_size, nb_worker=nb_worker, pickle_safe=pickle_safe, verbose=1)

    def evaluate_on_generator(self, samples_to_test):
        scores = self.model.evaluate_generator(self.batch_generator.generate_test_batch(), val_samples=samples_to_test)
        print("Accuracy: %.2f%%" % (scores[1] * 100))

    def predict_tokenized_sentence(self, tokenized_sentence, pad=False):
        X = self.w2v_reader.encode_sentence(tokenized_sentence)

        predictions = self.model.predict(X, batch_size=1)

        tags = self.w2v_reader.decode_prediction_sequence(predictions[0])

        if not pad:
            tags = tags[-len(tokenized_sentence):]

        return zip(tokenized_sentence, tags)

    def predict_sentence(self, sentence, pad=False):
        tokenized_sentence = tokenizer.tokenize_word(sentence)

        return self.predict_sentence_tokenized(tokenized_sentence, pad)

    def save_model(self):
        pass  # TODO: implement

    def save(self, model_fp, w2v_reader_file, batch_gen_file):
        print('Saving model...')
        self.model.save(model_fp)
        self.save_w2v_reader(w2v_reader_file)
        self.save_batch_generator(batch_gen_file)

    def load(self, model_fp, w2v_reader_file, batch_gen_file):
        print('Loading model...')
        self.model = load_model(model_fp)
        self.load_w2v_reader(w2v_reader_file)
        self.load_batch_generator(batch_gen_file)
        self.w2v_reader.tag_vector_map = self.batch_generator.tag_vector_map  # TODO: workaround

    def save_w2v_reader(self, fp):
        with open(fp, 'wb') as output_f:
            pickle.dump(self.w2v_reader, output_f, -1)

    def load_w2v_reader(self, fp):
        with open(fp, 'rb') as in_f:
            self.w2v_reader = pickle.load(in_f)

    def save_batch_generator(self, fp):
        with open(fp, 'wb') as output_f:
            pickle.dump(self.batch_generator, output_f, -1)

    def load_batch_generator(self, fp):
        with open(fp, 'rb') as in_f:
            self.batch_generator = pickle.load(in_f)
