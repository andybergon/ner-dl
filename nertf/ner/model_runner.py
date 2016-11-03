import net_settings as ns
import path_settings as s
from batch_generator import BatchGenerator
from model import NERModel
from word2vec_reader import Word2VecReader


class ModelRunner:
    def __init__(self, class_list, max_sentence_len):
        self.class_list = class_list
        self.max_sentence_len = max_sentence_len

        self.ner_model = None

    def train(self, use_generator=False):
        word2vec_txt_filepath = s.WORD2VEC_TXT_FILE
        training_filepath = s.TRAINING_FILE
        test_filepath = s.TEST_FILE
        class_list = self.class_list
        max_sentence_len = self.max_sentence_len

        print(">> Loading word2vec vectors from file...")
        w2v_reader = Word2VecReader(word2vec_txt_filepath)
        batch_generator = BatchGenerator(w2v_reader, training_filepath, test_filepath, class_list, max_sentence_len)

        dropout = ns.DROPOUT
        reg_alpha = ns.REG_ALPHA
        layers = ns.LAYERS

        print(">> Compiling model... dropout = {}, reg_alpha = {}, layers = {}".format(dropout, reg_alpha, layers))
        self.ner_model = NERModel(w2v_reader, batch_generator)
        self.ner_model.compile(dropout=dropout, reg_alpha=reg_alpha, layers=layers)

        # ner_model.print_summary()

        if use_generator:
            batch_size = ns.BATCH_SIZE_GENERATOR
            nb_epoch = ns.NB_EPOCH_GENERATOR
            max_q_size = ns.MAX_Q_SIZE
            nb_worker = ns.NB_WORKER
            pickle_safe = ns.PICKLE_SAFE

            print(">> Training model... (using fit_generator) - epochs = {}, batch_size = {}"
                  .format(nb_epoch, batch_size))
            self.ner_model.train_on_generator(nb_epoch=nb_epoch,
                                              samples_per_epoch=batch_size,
                                              max_q_size=max_q_size,
                                              nb_worker=nb_worker,
                                              pickle_safe=pickle_safe)
        else:
            batch_size = ns.BATCH_SIZE
            nb_epoch = ns.NB_EPOCH
            save_every_nb_iterations = ns.SAVE_EVERY_NB_ITERATIONS

            print(">> Training model... (using fit) -  epochs = {}, batch_size = {}".format(nb_epoch, batch_size))
            self.ner_model.train_on_batches(batch_size=batch_size,
                                            nb_epoch=nb_epoch,
                                            save_every_nb_iterations=save_every_nb_iterations)

    def evaluate(self):
        samples_to_test = ns.SAMPLES_TO_TEST

        print(">> Evaluating model...")
        self.ner_model.evaluate_on_generator(samples_to_test=samples_to_test)

    def save(self):
        print(">> Saving model...")
        self.ner_model.save()
