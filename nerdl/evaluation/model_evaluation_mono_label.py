from __future__ import division

from settings import path_settings


class EvaluatorMonoLabel:
    def __init__(self, model):
        self.ner_model = model
        self.test_filepath = path_settings.TEST_FILE
        self.stats = {}

    def evaluate_model(self):
        sentence_num = 0

        tot_nb_tags = 0
        tot_true_positive = 0
        tot_true_negative = 0
        tot_false_positive = 0
        tot_false_negative = 0
        tot_wrong_entity = 0
        tot_nil_false_positive = 0

        words, tags = [], []

        with open(self.test_filepath, 'r') as f:
            for line in f:
                if line != '\n':
                    word, tag = line.replace('\n', '').split('\t')
                    words.append(word)
                    tags.append(tag)
                else:
                    sentence_num += 1

                    nb_tags = 0
                    true_positive = 0
                    true_negative = 0
                    false_positive = 0
                    false_negative = 0
                    wrong_entity = 0
                    nil_false_positive = 0

                    predicted_tags_tuples = self.ner_model.predict_tokenized_sentence(words)
                    predicted_tags = (i[1] for i in predicted_tags_tuples)  # can use generator (...) for performance

                    # zip ok if lists not too big
                    for correct, predicted in zip(tags, predicted_tags):
                        nb_tags += 1

                        if correct == predicted:
                            if correct != 'NIL' and correct != 'O':
                                true_positive += 1
                            else:
                                true_negative += 1
                        else:
                            if correct == 'O':
                                false_positive += 1
                            elif predicted == 'O':
                                false_negative += 1
                            else:  # correct and predict != 'O'
                                wrong_entity += 1

                        if predicted == 'NIL':
                            nil_false_positive += 1

                    words = []
                    tags = []

                    tot_nb_tags += nb_tags
                    tot_true_positive += true_positive
                    tot_true_negative += true_negative
                    tot_false_positive += false_positive
                    tot_false_negative += false_negative
                    tot_wrong_entity += wrong_entity
                    tot_nil_false_positive += nil_false_positive

                    if sentence_num % 100 == 0:
                        self.stats = {
                            'TP': tot_true_positive,
                            'TN': tot_true_negative,
                            'FP': tot_false_positive,
                            'FN': tot_false_negative,
                            'WE': tot_wrong_entity,
                            'NIL_FP': tot_nil_false_positive,
                            'TOT_TAGS': tot_nb_tags,
                            'TOT_SENT': sentence_num
                        }

                        self.print_stats()

    def print_stats(self):
        tp = self.stats['TP']
        tn = self.stats['TN']
        fp = self.stats['FP']
        fn = self.stats['FN']
        we = self.stats['WE']
        nil_fp = self.stats['NIL_FP']
        tot_tags = self.stats['TOT_TAGS']
        tot_sent = self.stats['TOT_SENT']

        print(
            'True Positive (correct == predict != O): {}\n'
            'True Negative (correct == predict == O): {}\n'
            'False Positive (correct == O and predict !=O): {}\n'
            'False Negative (correct != O and predict == O): {}\n'
            'Wrong Entity (correct != predict != O): {}\n'
            'NIL False Positive: {}\n'
            'Total Tags: {}\n'
            'Total Sentences: {}\n\n'.format(tp, tn, fp, fn, we, nil_fp, tot_tags, tot_sent)
        )

        tot_pres = tp + fn + we
        perc_tp = tp / tot_pres
        perc_we = we / tot_pres
        perc_fn = fn / tot_pres

        print('Recognized correctly: {}\t{}\n'
              'Recognized as another entity: {}\t{}\n'
              'Not recognized: {}\t{}\n'.format(tp, perc_tp, we, perc_we, fn, perc_fn))
