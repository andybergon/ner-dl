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
from keras.callbacks import ModelCheckpoint

import settings
import tokenizer

np.random.seed(0)  # for debugging


class NERModel:
    def __init__(self, reader=None, generator=None):
        self.model = None

        self.w2v_reader = reader
        self.batch_generator = generator

        self.ner_model_fp = settings.MODEL_FILE
        self.word2vec_reader_fp = settings.W2V_READER_FILE
        self.batch_generator_fp = settings.BATCH_GENERATOR_FILE

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

    def train_on_batches(self, batch_size, nb_epoch, save_every_nb_iterations=0):
        nb_curr_iteration = 0

        print('Saving initial model, w2v reader and batch generator...')
        self.save()

        for epoch in range(nb_epoch):
            print('Epoch {}'.format(epoch + 1))

            for X_batch, Y_batch in self.batch_generator.generate_multiple_training_batch(batch_size=batch_size):
                self.model.fit(X_batch, Y_batch, batch_size=batch_size, nb_epoch=nb_epoch)

                nb_curr_iteration += 1

                if save_every_nb_iterations != 0 and nb_curr_iteration % save_every_nb_iterations == 0:
                    print('Saving weights... (every {} iterations)'.format(save_every_nb_iterations))
                    self.save_only_model()

    def train_on_generator(self, samples_per_epoch, nb_epoch, max_q_size, nb_worker, pickle_safe):
        generator = self.batch_generator.generate_training_batch()

        cp_fp = settings.MODEL_FILE
        checkpoint = ModelCheckpoint(cp_fp, monitor='val_acc', verbose=1, save_best_only=False, mode='max')
        callbacks = [checkpoint]

        self.model.fit_generator(generator=generator,
                                 samples_per_epoch=samples_per_epoch,
                                 nb_epoch=nb_epoch,
                                 verbose=1,
                                 callbacks=callbacks,
                                 max_q_size=max_q_size,
                                 nb_worker=nb_worker,
                                 pickle_safe=pickle_safe)

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

    # SAVE & LOAD
    def save_only_model(self):
        print('Saving model only...')
        self.model.save(self.ner_model_fp)

    def save(self):
        print('Saving model...')
        self.model.save(self.ner_model_fp)
        self.save_w2v_reader()
        self.save_batch_generator()

    def load(self):
        print('Loading model...')
        self.model = load_model(self.model_fp)
        self.load_w2v_reader()
        self.load_batch_generator()

        self.w2v_reader.tag_vector_map = self.batch_generator.tag_vector_map  # TODO: workaround

    def save_w2v_reader(self):
        with open(self.word2vec_reader_fp, 'wb') as output_f:
            pickle.dump(self.w2v_reader, output_f, -1)

    def load_w2v_reader(self):
        with open(self.word2vec_reader_fp, 'rb') as in_f:
            self.w2v_reader = pickle.load(in_f)

    def save_batch_generator(self):
        with open(self.batch_generator_fp, 'wb') as output_f:
            pickle.dump(self.batch_generator, output_f, -1)

    def load_batch_generator(self):
        with open(self.batch_generator_fp, 'rb') as in_f:
            self.batch_generator = pickle.load(in_f)
