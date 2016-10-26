import net_settings as ns
import settings as s
from batch_generator import BatchGenerator
from model import NERModel
from word2vec_reader import Word2VecReader


def train_evaluate_save(class_list, max_sentence_len, evaluate_model=True, save_model=True):
    dropout = ns.DROPOUT
    reg_alpha = ns.REG_ALPHA
    layers = ns.LAYERS

    nb_epoch = ns.NB_EPOCH
    batch_size = ns.BATCH_SIZE
    max_q_size = ns.MAX_Q_SIZE
    nb_worker = ns.NB_WORKER
    pickle_safe = ns.PICKLE_SAFE

    samples_to_test = ns.SAMPLES_TO_TEST

    word2vec_txt_filepath = s.WORD2VEC_TXT_FILE
    training_filepath = s.TRAINING_FILE
    test_filepath = s.TEST_FILE
    ner_model_filepath = s.MODEL_FILE
    word2vec_reader_filepath = s.W2V_READER_FILE
    batch_generator_filepath = s.BATCH_GENERATOR_FILE

    print(">> Loading word2vec vectors from file...")
    w2v_reader = Word2VecReader(word2vec_txt_filepath)
    batch_generator = BatchGenerator(w2v_reader, training_filepath, test_filepath, class_list,
                                     max_sentence_len, batch_size)

    print(">> Training model... epochs = {}, layers = {}".format(nb_epoch, layers))
    ner_model = NERModel(w2v_reader, batch_generator)
    ner_model.compile(dropout=dropout, reg_alpha=reg_alpha, layers=layers)
    # ner_model.print_summary()
    ner_model.train_on_generator(nb_epoch=nb_epoch, samples_per_epoch=batch_size, max_q_size=max_q_size,
                                 nb_worker=nb_worker, pickle_safe=pickle_safe)

    if evaluate_model:
        print(">> Evaluating model...")
        ner_model.evaluate_on_generator(samples_to_test=samples_to_test)

    if save_model:
        print(">> Saving model...")
        ner_model.save(ner_model_filepath, word2vec_reader_filepath, batch_generator_filepath)

    print(">> Done.")
