import settings
from model import NERModel
from stanford_ner import StanfordNERModel


class Evaluator:
    def __init__(self, own_model=True):
        self.test_filepath = settings.TEST_FILE

        if own_model:
            ner_model_file = settings.MODEL_FILE
            w2v_reader_file = settings.W2V_READER_FILE
            batch_gen_file = settings.BATCH_GEN_FILE

            self.ner_model = NERModel()
            self.ner_model.load(ner_model_file, w2v_reader_file, batch_gen_file)
        else:
            self.ner_model = StanfordNERModel

    def evaluate_model(self):
        sentence_num = 0
        nb_total_correct = 0
        nb_total_correct_entity = 0
        nb_total_error = 0
        nb_total_error_entity = 0
        words, tags = [], []

        with open(self.test_filepath, 'r') as f:
            for line in f:
                if line != '\n':
                    word, tag = line.replace('\n', '').split('\t')
                    words.append(word)
                    tags.append(tag)
                else:
                    sentence_num += 1

                    nb_correct = 0
                    nb_correct_entity = 0
                    nb_error = 0
                    nb_error_entity = 0

                    sentence = ' '.join(words)  # TODO: use detokenizer

                    predicted_tags = self.ner_model.predict_sentence(sentence)

                    # zip ok if lists not so big
                    for correct, predicted in zip(tags, predicted_tags):
                        if correct == predicted:
                            nb_correct += 1
                            if correct != 'NIL' and correct != 'O':
                                nb_correct_entity += 1
                        else:
                            nb_error += 1
                            if correct != 'NIL' and correct != 'O':
                                nb_error_entity += 1

                    words = []
                    tags = []

                    nb_total_correct += nb_correct
                    nb_total_correct_entity += nb_correct_entity
                    nb_total_error += nb_error
                    nb_total_error_entity += nb_error_entity

                    if sentence_num % 100 == 0:
                        print(
                            'Correct: {}\nCorrect Entities: {}\nErrors: {}\nErrors Entities: {}\nTotal: {}\n'.format(
                                nb_total_correct, nb_correct_entity, nb_total_error, nb_total_error_entity,
                                sentence_num))
