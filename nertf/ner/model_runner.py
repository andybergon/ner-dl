from batch_generator import BatchGenerator
from model import NERModel
from word2vec_reader import Word2VecReader


def train_evaluate_save(word2vec_filepath, training_filepath, test_filepath, ner_model_filepath, class_list,
                        max_sentence_len, save_model=True):
    nb_epoch = 3
    batch_size = 64

    dropout = 0.5
    reg_alpha = 0.000
    layers = 1

    samples_to_test = 1000
    max_q_size = 1

    print(">> Loading word2vec vectors from file...")
    w2v_reader = Word2VecReader(word2vec_filepath, training_filepath)
    batch_generator = BatchGenerator(w2v_reader, training_filepath, test_filepath, class_list,
                                     max_sentence_len, batch_size)

    print(">> Training model... epochs = {0}, layers = {1}".format(nb_epoch, layers))
    ner_model = NERModel(w2v_reader, batch_generator)
    ner_model.compile(dropout=dropout, reg_alpha=reg_alpha, layers=layers)
    # ner_model.print_summary()
    ner_model.train_on_generator(nb_epoch=nb_epoch, samples_per_epoch=batch_size, max_q_size=max_q_size)

    print(">> Evaluating model...")
    ner_model.evaluate_on_generator(samples_to_test=samples_to_test)

    if save_model:
        print(">> Saving model...")
        ner_model.save(ner_model_filepath)

    print(">> Done.")
