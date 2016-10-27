from __future__ import division

import settings
from nertf.ner.external_models.stanford_ner_model import StanfordNERModel
from nertf.ner.model import NERModel


class Comparator:
    def __init__(self, class_list):
        self.test_filepath = settings.TEST_FILE

        self.class_list = class_list
        self.sentence_num = 0
        self.stats_1 = {}
        self.stats_2 = {}
        self.stats = {}

        for entity_class in self.class_list:
            self.stats_1[entity_class] = {}
            self.stats_2[entity_class] = {}
            for entity_class_inner in self.class_list:
                self.stats_1[entity_class][entity_class_inner] = 0
                self.stats_2[entity_class][entity_class_inner] = 0

        for entity_class in self.class_list:
            # (only_1_correct, only_2_correct, both_correct, both_error, total_found)
            self.stats[entity_class] = [0, 0, 0, 0, 0]

        ner_model_file = settings.MODEL_FILE
        w2v_reader_file = settings.W2V_READER_FILE
        batch_gen_file = settings.BATCH_GENERATOR_FILE

        nn_ner_model = NERModel()
        nn_ner_model.load(ner_model_file, w2v_reader_file, batch_gen_file)

        stanford_ner_model = StanfordNERModel()

        self.model_1 = nn_ner_model
        self.model_2 = stanford_ner_model

    def compare_models(self, print_every=100):
        words, tags = [], []

        with open(self.test_filepath, 'r') as f:
            for line in f:
                if line != '\n':
                    word, tag = line.replace('\n', '').split('\t')
                    words.append(word)
                    tags.append(tag)
                else:
                    self.sentence_num += 1

                    model_1_predictions = self.model_1.predict_tokenized_sentence(words)
                    model_2_predictions = self.model_2.predict_tokenized_sentence(words)

                    predicted_tags_1 = [i[1] for i in model_1_predictions]  # can use generator (...) for performance
                    predicted_tags_2 = [i[1] for i in model_2_predictions]  # can use generator (...) for performance

                    if not (len(tags) == len(predicted_tags_1) == len(predicted_tags_2)):
                        raise ValueError('Correct and Prediction length different!')

                    # zip ok if lists not too big
                    for correct, predict_1, predict_2 in zip(tags, predicted_tags_1, predicted_tags_2):
                        self.stats_1[correct][predict_1] += 1
                        self.stats_2[correct][predict_2] += 1

                        if correct == predict_1 == predict_2:
                            self.stats[correct][2] += 1
                        elif correct == predict_1:
                            self.stats[correct][0] += 1
                        elif correct == predict_2:
                            self.stats[correct][1] += 1
                        else:
                            self.stats[correct][3] += 1

                        self.stats[correct][4] += 1

                    words = []
                    tags = []

                    print('Sentence #{} processed'.format(self.sentence_num))

                    if print_every > 0 and self.sentence_num % print_every == 0:
                        self.print_stats()
                        self.print_stats_perc()

    def print_stats(self):

        print('Model 1:')
        for correct_class in self.class_list:
            print('{:>6}\t{}'.format(correct_class, self.stats_1[correct_class]))

        print('Model 2:')
        for correct_class in self.class_list:
            print('{:>6}\t{}'.format(correct_class, self.stats_2[correct_class]))

        print('Model Comparison:')
        print('{:>6}\t(only_1_correct, only_2_correct, both_correct, both_error, total_found)'.format('tag'))
        for entity_class in self.class_list:
            print('{:>6}\t{}'.format(entity_class, self.stats[entity_class]))

    def print_stats_perc(self):

        print('Model 1:')
        self.print_perc(self.stats_1)

        print('Model 2:')
        self.print_perc(self.stats_2)

        print_dict = self.stats.copy()

        tot = [0, 0, 0, 0, 0]
        for key in print_dict:
            tot = [x + y for x, y in zip(tot, print_dict[key])]

        print_dict['TOTAL'] = tot

        print('Model Comparison:')
        print('{:>6}\t(only_1_correct, only_2_correct, both_correct, both_error)'.format('tag'))

        for entity_class in self.class_list:
            tup = print_dict[entity_class]

            if tup[4] != 0:
                only_1_perc = tup[0] / tup[4]
                only_2_perc = tup[1] / tup[4]
                both_correct_perc = tup[2] / tup[4]
                both_error_perc = tup[3] / tup[4]
                print('{:>6}\t{:.1%}\t{:.1%}\t{:.1%}\t{:.1%}'
                      .format(entity_class, only_1_perc, only_2_perc, both_correct_perc, both_error_perc))
            else:
                print('{:>6}\t{}\t{}\t{}\t{}'.format(entity_class, 'N.A', 'N.A', 'N.A', 'N.A'))

    def print_perc(self, stats_dict):
        for correct_class in self.class_list:
            sum_ok = sum(stats_dict[correct_class].values())
            if sum_ok != 0:
                perc_correct_dict = {k: '{:.1%}'.format(v / sum_ok) for k, v in stats_dict[correct_class].items()}
                print('{:>6}\t{}'.format(correct_class, perc_correct_dict))
            else:
                perc_correct_dict = {k: 'N.A.' for k, v in stats_dict[correct_class].items()}
                print('{:>6}\t{}'.format(correct_class, perc_correct_dict))
