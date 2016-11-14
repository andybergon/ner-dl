from nerdl.ner.models.figer.figer_client_socket import FigerSocket
from nerdl.ner.models.model import Model
from nerdl.ner.utils import tokenizer


class FigerNERModel(Model):
    def __init__(self, nb_classes=4):
        self.socket = FigerSocket()

    def predict_tokenized_sentence(self, tokenized_sentence):
        untokenized_sentence = tokenizer.untokenize_word(tokenized_sentence)
        prediction = self.socket.request_prediction(untokenized_sentence)

        if len(prediction) != len(tokenized_sentence):
            print('Prediction and tokenized sentence have different lengths!')
            raise(ValueError, 'Sentence and Prediction have different lengths. Probably worng tokenization of FIGER.')

        prediction = cutoff_top(prediction)

        return prediction

    def predict_sentence(self, sentence):
        tokenized_sentence = tokenizer.tokenize_word(sentence)

        return self.predict_tokenized_sentence(tokenized_sentence)


def cutoff_top(prediction):
    prediction = normalize_scores(prediction)
    word_types = []

    # TODO: top x
    for word_typescore in prediction:
        types = []
        for type_score in word_typescore[1]:
            types.append(type_score[0])
        word_types.append((word_typescore[0], types))

    return word_types


def normalize_scores(prediction):
    normalized_prediction = []

    for pred_tuple in prediction:
        word, types_scores = pred_tuple
        sum_score = 0
        new_types_scores = []
        for type, score in types_scores:
            sum_score += float(score)
        for type, score in types_scores:
            new_type_score = (type, float(score) / sum_score)
            new_types_scores.append(new_type_score)
        normalized_prediction.append((word, new_types_scores))

    return normalized_prediction
