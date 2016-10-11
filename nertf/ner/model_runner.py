from model import NERModel
from word2vec_reader import Word2VecReader


def train_evaluate_save(word2vec_filepath, training_filepath, ner_model_filepath):
    epochs = 10
    dropout = 0.5
    reg_alpha = 0.000
    layers = 2

    print(">> Loading word2vec vectors from file...")
    w2v_reader = Word2VecReader(word2vec_filepath, training_filepath)
    X, Y = w2v_reader.get_data()
    print(X.shape)
    print(Y.shape)

    print(">> Training model... epochs = {0}, layers = {1}".format(epochs, layers))
    ner_model = NERModel(w2v_reader)
    ner_model.train(epochs=epochs, dropout=dropout, reg_alpha=reg_alpha, layers=layers)

    print(">> Evaluating model...")
    ner_model.evaluate()

    print(">> Saving model...")
    ner_model.save(ner_model_filepath)

    print(">> Done.")
