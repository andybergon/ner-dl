class Model:
    def __init__(self):
        pass

    def predict_with_stanford_detection(self, tokenized_sentence, threshold=0.1):
        pass

    def predict_given_bio(self, word_bio, threshold=0):
        pass

    def predict_scores_given_bio(self, word_bio):
        pass

    def predict_entities(self, sentence):
        pass

    def predict_sentence(self, sentence):
        pass

    def predict_tokenized_entities(self, tokenized_sentence):
        pass

    def predict_tokenized_sentence(self, tokenized_sentence):
        pass
