from __future__ import division

from settings import path_settings
from settings import settings


class EvaluatorMultiLabel:
    def __init__(self, model):
        self.ner_model = model

        self.class_list = settings.EVALUATION_CLASS_LIST
        self.test_filepath = path_settings.TEST_FILE

        # loose micro correct stats, for Recall. 0 not present in predict, 1 present in predict.
        self.lmi_correct = {}
        # loose micro predict stats, for Precision. 0 not present in correct, 1 present in correct.
        self.lmi_predict = {}

        self.initialize_stats()

    def initialize_stats(self):
        for tag_class in self.class_list:
            self.lmi_correct[tag_class] = [0, 0]
            self.lmi_predict[tag_class] = [0, 0]

    def evaluate_model(self, test_sentences_nb=1000, print_every=100):
        """

        :param test_sentences_nb: Sentences to test. 0 for all test file.
        :param print_every: Print stats frequency. 0 never print.
        :return: Precision, Recall, F1 Score
        """
        sentence_num = 0
        sentence_eval_num = 0

        words, tags = [], []

        with open(self.test_filepath, 'r') as f:
            for line in f:
                if line != '\n':
                    word, tag = line.replace('\n', '').split('\t')
                    words.append(word)
                    tags.append(tag.split(','))
                else:
                    sentence_num += 1

                    try:
                        predicted_tags_tuples = self.ner_model.predict_tokenized_sentence(words)

                        predicted_tags = (i[1] for i in
                                          predicted_tags_tuples)  # can use generator (...) for performance

                        # self.calculate_strict(tags, predicted_tags)
                        # self.calculate_loose_macro(tags, predicted_tags)
                        self.calculate_loose_micro(tags, predicted_tags)
                        sentence_eval_num += 1

                    except ValueError:
                        continue
                    finally:
                        words = []
                        tags = []

                        if sentence_num % print_every == 0 and print_every != 0:
                            print('Evaluated sentences: {}/{}'.format(sentence_eval_num, sentence_num))
                            self.print_stats()

                        if sentence_num == test_sentences_nb and test_sentences_nb != 0:
                            print('Evaluated sentences: {}/{}'.format(sentence_eval_num, sentence_num))
                            p, r, f1 = self.print_stats()
                            return p, r, f1

            print('Evaluated sentences: {}/{}'.format(sentence_eval_num, sentence_num))
            p, r, f1 = self.print_stats()
            return p, r, f1

    def calculate_strict_micro(self, correct_tags, predicted_tags):
        pass

    def calculate_loose_macro(self, correct_tags, predicted_tags):
        pass

    def calculate_loose_micro(self, correct_tags, predicted_tags):
        # zip ok if lists not too big
        for correct, predicted in zip(correct_tags, predicted_tags):
            for correct_tag in correct:
                if correct_tag in predicted:
                    self.lmi_correct[correct_tag][1] += 1
                else:
                    self.lmi_correct[correct_tag][0] += 1

            for predicted_tag in predicted:
                if predicted_tag in correct:
                    self.lmi_predict[predicted_tag][1] += 1
                else:
                    self.lmi_predict[predicted_tag][0] += 1

    def print_stats(self):
        return self.print_loose_micro_stats()

    def print_loose_micro_stats(self):
        correct_yes = 0
        correct_no = 0
        predict_yes = 0
        predict_no = 0

        for tag_class in self.class_list:
            if tag_class != 'O' and tag_class != 'NIL':
                correct_yes += self.lmi_correct[tag_class][1]
                correct_no += self.lmi_correct[tag_class][0]
                predict_yes += self.lmi_predict[tag_class][1]
                predict_no += self.lmi_predict[tag_class][0]

        correct_perc = correct_yes / (correct_yes + correct_no)
        predict_perc = predict_yes / (predict_yes + predict_no)
        f1_score = 2 * (predict_perc * correct_perc) / (predict_perc + correct_perc)

        o_fp = self.lmi_predict['O'][0]
        o_tn = 0  # TODO: complicated and expensive to calculate, must count total number of entities
        o_fpr = o_fp / (o_fp + o_tn)
        o_fn = self.lmi_correct['O'][0]
        o_tp = self.lmi_correct['O'][1]
        o_fnr = o_fn / (o_tp + o_fn)

        print('--------------------------------------------------')
        print('LOOSE MICRO STATS')
        print('Correct entities found: {}/{} - {:.0%}'.format(correct_yes, correct_no, correct_perc))
        print('Predicted entities correct: {}/{} - {:.0%}'.format(predict_yes, predict_no, predict_perc))
        print('Precision: {}\nRecall: {}\nF1 Score: {}'.format(predict_perc, correct_perc, f1_score))
        print('O Tag - FP: {} {}, FN: {} {}'.format(o_fp, o_fpr, o_fn, o_fnr))
        print('--------------------------------------------------')

        return predict_perc, correct_perc, f1_score  # precision, recall, f1 score
