from __future__ import division

from settings import settings


class EvaluatorEntities:
    def __init__(self, sentence_iterator_correct, sentence_iterator_predict, correct_s2e, predict_s2e):
        self.class_list = settings.EVALUATION_CLASS_LIST

        self.si_correct = sentence_iterator_correct
        self.si_predict = sentence_iterator_predict

        self.correct_s2e = correct_s2e
        self.predict_s2e = predict_s2e

        # loose micro correct stats, for Recall. 0 not present in predict, 1 present in predict.
        self.lmi_correct = {}
        # loose micro predict stats, for Precision. 0 not present in correct, 1 present in correct.
        self.lmi_predict = {}

        self.initialize_stats()

    def initialize_stats(self):
        for tag_class in self.class_list:
            self.lmi_correct[tag_class] = [0, 0]
            self.lmi_predict[tag_class] = [0, 0]

    def evaluate(self, test_sentences_nb=1000, print_every=100):
        """

        :param test_sentences_nb: Sentences to test. 0 for all test file.
        :param print_every: Print stats frequency. 0 never print.
        :return: Precision, Recall, F1 Score
        """
        sentence_num = 0

        while self.si_correct.is_file_open or self.si_predict.is_file_open:
            sent_correct = self.si_correct.next()
            sent_predict = self.si_predict.next()

            entities_correct = self.correct_s2e.convert_to_entities(sent_correct)
            entities_predict = self.predict_s2e.convert_to_entities(sent_predict)

            # self.calculate_strict(word_tag_prediction)
            # self.calculate_loose_macro(word_tag_prediction)
            self.calculate_loose_micro(entities_correct, entities_predict)

            sentence_num += 1

            if print_every != 0 and sentence_num % print_every == 0:
                print('Evaluated sentences: {}/{}'.format(sentence_num, test_sentences_nb))
                self.print_stats()

            if test_sentences_nb != 0 and sentence_num == test_sentences_nb:
                print('Evaluated sentences: {}/{}'.format(sentence_num, test_sentences_nb))
                p, r, f1 = self.print_stats()
                return p, r, f1

        # if test_sentences_nb == 0 or sentence_num < print_every:
        print('Evaluated sentences: {}/{}'.format(sentence_num, test_sentences_nb))
        p, r, f1 = self.print_stats()

        return p, r, f1

    def calculate_strict_micro(self, entities_correct, entities_predict):
        pass

    def calculate_loose_macro(self, entities_correct, entities_predict):
        pass

    def calculate_loose_micro(self, entities_tags_correct, entities_tags_predict):

        # RECALL
        entities_predict = [i[0] for i in entities_tags_predict]
        for entity, types in entities_tags_correct:
            if entity in entities_predict:
                # TODO: manage duplicate entities, removing entity from entities
                types_predict = [i[1] for i in entities_tags_predict if i[0] == entity][0]
                for type in types:
                    if type in types_predict:
                        self.lmi_correct[type][1] += 1
                    else:
                        self.lmi_correct[type][0] += 1
            else:
                # for type in types:
                #     self.lmi_correct[type][0] += 1
                pass  # comment for: entity not found == don't count

        # PRECISION
        entities_correct = [i[0] for i in entities_tags_correct]
        for entity, types in entities_tags_predict:
            if entity in entities_correct:
                # TODO: manage duplicate entities, removing entity from entities
                types_correct = [i[1] for i in entities_tags_correct if i[0] == entity][0]
                for type in types:
                    if type in types_correct:
                        self.lmi_predict[type][1] += 1
                    else:
                        self.lmi_predict[type][0] += 1
            else:
                # for type in types:
                #     self.lmi_predict[type][0] += 1
                pass  # comment for: entity not found == don't count

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

        print('--------------------------------------------------')
        print('LOOSE MICRO STATS')
        print('Correct tags found: {}/{} - {:.0%}'.format(correct_yes, correct_no, correct_perc))
        print('Predicted tags correct: {}/{} - {:.0%}'.format(predict_yes, predict_no, predict_perc))
        print('Precision:\t{}\nRecall:\t{}\nF1 Score:\t{}'.format(predict_perc, correct_perc, f1_score))
        print('--------------------------------------------------')

        return predict_perc, correct_perc, f1_score  # precision, recall, f1 score
