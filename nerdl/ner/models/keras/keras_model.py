import numpy as np
from keras.callbacks import ModelCheckpoint
from keras.layers import Dense  # TODO: slow. necessary to load on import?
from keras.layers import LSTM
from keras.layers.core import Dropout
from keras.layers.wrappers import Bidirectional
from keras.layers.wrappers import TimeDistributed
from keras.models import Sequential
from keras.models import load_model
from keras.regularizers import l2

from batch_generator import BatchGenerator
from nerdl.ner.models.model import Model
from nerdl.ner.sentence2entities import Sentence2Entities
from nerdl.ner.utils import tokenizer
from nerdl.ner.w2v.tag2vec_reader import Tag2VecReader
from nerdl.ner.w2v.word2vec_reader import Word2VecReader
from settings import net_settings as ns
from settings import path_settings

np.random.seed(0)  # for debugging


class KerasNERModel(Model):
    def __init__(self, tagger=None):
        self.model = None

        self.w2v_reader = Word2VecReader()  # TODO: compare with saving python object that is less flexible
        self.t2v_reader = Tag2VecReader()
        self.tagger = tagger
        self.s2e = Sentence2Entities(auto_detect=True)  # when all migrated to BIO tag, pass True

        self.batch_generator = None  # can be a parameter of methods

        self.ner_model_fp = path_settings.MODEL_FILE
        self.ner_model_load_fp = path_settings.MODEL_TO_LOAD_FILE

    def print_summary(self):
        print(self.model.summary())

    def compile(self, dropout=0.2, reg_alpha=0.0, units=128, layers=1):

        # (max_length, w2v_length), e.g. (95,300)
        input_shape = (self.batch_generator.max_sentence_len, self.w2v_reader.n_features)
        # e.g. (6)
        output_dim = self.t2v_reader.nb_classes
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

    # TRAINING
    def train(self, use_generator=True, resume_train=False):

        batch_generator = BatchGenerator(self.w2v_reader, self.t2v_reader, self.tagger)
        self.batch_generator = batch_generator

        dropout = ns.DROPOUT
        reg_alpha = ns.REG_ALPHA
        units = ns.UNITS
        layers = ns.LAYERS

        print('>> Compiling model... dropout = {}, reg_alpha = {}, units = {}, layers = {}'
              .format(dropout, reg_alpha, units, layers))

        self.compile(dropout=dropout, reg_alpha=reg_alpha, units=units, layers=layers)

        # ner_model.print_summary()

        if use_generator:
            batch_size = ns.BATCH_SIZE_GENERATOR
            nb_epoch = ns.NB_EPOCH_GENERATOR
            max_q_size = ns.MAX_Q_SIZE
            nb_worker = ns.NB_WORKER
            pickle_safe = ns.PICKLE_SAFE

            print('>> Training model... (using fit_generator) - epochs = {}, batch_size = {}'
                  .format(nb_epoch, batch_size))
            self.train_on_generator(resume_train=resume_train,
                                    nb_epoch=nb_epoch,
                                    samples_per_epoch=batch_size,
                                    max_q_size=max_q_size,
                                    nb_worker=nb_worker,
                                    pickle_safe=pickle_safe)
        else:
            batch_size = ns.BATCH_SIZE
            nb_epoch = ns.NB_EPOCH
            save_every_nb_iterations = ns.SAVE_EVERY_NB_ITERATIONS

            print('>> Training model... (using fit) -  epochs = {}, batch_size = {}'
                  .format(nb_epoch, batch_size))
            self.train_on_batches(batch_size=batch_size,
                                  nb_epoch=nb_epoch,
                                  save_every_nb_iterations=save_every_nb_iterations)

    def resume_train(self):
        self.load()
        self.train(resume_train=True)

    def train_on_generator(self, resume_train, samples_per_epoch, nb_epoch, max_q_size, nb_worker, pickle_safe):
        generator = self.batch_generator.generate_training_batch(resume_gen=resume_train)

        cp_fp = path_settings.MODEL_FILE
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

    def train_on_batches(self, batch_size, nb_epoch, save_every_nb_iterations=0):
        nb_curr_iteration = 0

        print('Saving initial model, w2v reader and batch generator...')
        self.save()

        for epoch in range(nb_epoch):
            print('Epoch {}'.format(epoch + 1))

            for X_batch, Y_batch in self.batch_generator.generate_training_batch(batch_size=batch_size):
                self.model.fit(X_batch, Y_batch, batch_size=batch_size, nb_epoch=nb_epoch)

                nb_curr_iteration += 1

                if save_every_nb_iterations != 0 and nb_curr_iteration % save_every_nb_iterations == 0:
                    print('Saving weights... (every {} iterations)'.format(save_every_nb_iterations))
                    self.save_only_model()

    # PREDICTION
    # TODO: fix
    def predict_entities(self, sentence):
        tagged_sentence = self.predict_sentence(sentence, False)
        return self.s2e.convert_to_entities(tagged_sentence)

    # TODO: fix
    def predict_tokenized_entities(self, tokenized_sentence):
        tagged_sentence = self.predict_tokenized_sentence(tokenized_sentence, False)
        return self.s2e.convert_to_entities(tagged_sentence)

    def predict_sentence(self, sentence, pad=False):
        tokenized_sentence = tokenizer.tokenize_in_words(sentence)
        return self.predict_tokenized_sentence(tokenized_sentence, pad)

    def predict_tokenized_sentence(self, tokenized_sentence, pad=False):
        X = self.w2v_reader.encode_sentence(tokenized_sentence)
        predictions = self.model.predict(X, batch_size=1)
        tags = self.t2v_reader.decode_prediction(predictions[0])

        if not pad:
            tags = tags[-len(tokenized_sentence):]

        return zip(tokenized_sentence, tags)

    # EVALUATION
    def evaluate(self):
        samples_to_test = ns.SAMPLES_TO_TEST

        print('>> Evaluating model...')
        self.evaluate_on_generator(samples_to_test=samples_to_test)

    def evaluate_on_generator(self, samples_to_test):
        scores = self.model.evaluate_generator(self.batch_generator.generate_test_batch(), val_samples=samples_to_test)
        print('Accuracy: %.2f%%' % (scores[1] * 100))

    # SAVE & LOAD
    def save(self):
        print('Saving entire model object...')
        self.save_only_model()

    def save_only_model(self):
        print('Saving model only...')
        self.model.save(self.ner_model_fp)

    def load(self):
        print('Loading entire model object...')
        self.load_only_model()

    def load_only_model(self):
        print('Loading model only...')
        self.model = load_model(self.ner_model_load_fp)
