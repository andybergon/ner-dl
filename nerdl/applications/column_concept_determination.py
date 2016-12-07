from __future__ import division

from nerdl.ner.utils import tokenizer
from settings import path_settings


def calculate_difference(predicted_types, correct_types):
    precision_correct = 0
    precision_error = 0

    for pred_type in predicted_types:
        if pred_type in correct_types:
            precision_correct += 1
        else:
            precision_error += 1

    recall_correct = 0
    recall_error = 0

    for corr_type in correct_types:
        if corr_type in predicted_types:
            recall_correct += 1
        else:
            recall_error += 1

    precision = precision_correct / (precision_correct + precision_error) \
        if (precision_correct + precision_error) > 0 else 0
    recall = recall_correct / (recall_correct + recall_error) if (recall_correct + recall_error) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1


class CCD:
    def __init__(self, model):
        self.model = model

        self.persons = {}
        self.others = {}

        self.persons_stats = {}
        self.others_stats = {}

        self.load_person_lector()
        self.load_other_lector()

    def load_person_lector(self):
        with open(path_settings.PERSON_LECTOR_FILE) as f:
            for line in f:
                mid, name, types = line.rstrip().split('\t')
                types = types.split(',')
                self.persons[mid] = name, types

    def load_other_lector(self):
        with open(path_settings.OTHERS_LECTOR_FILE) as f:
            for line in f:
                mid, name, types = line.rstrip().split('\t')
                types = types.split(',')
                self.others[mid] = name, types

    def predict_persons_multiple_thresholds(self, is_person, person_nb, retrieval_threshold, threshold_list):
        thresholds_stats = {}

        for threshold in threshold_list:
            print('THRESHOLD = {}'.format(threshold))
            p, r, f1 = self.predict_persons_or_others(is_person=is_person,
                                                      person_nb=person_nb,
                                                      retrieval_threshold=retrieval_threshold,
                                                      threshold=threshold)
            thresholds_stats[threshold] = p, r, f1

        print('Easy Excel Import:')
        for k, v in sorted(thresholds_stats.items()):
            print('{}\t{}\t{}\t{}'.format(k, v[0], v[1], v[2]))

        return thresholds_stats

    def predict_persons_or_others(self, is_person=True, person_nb=100, min_sent=5, max_sent=250, threshold=0.5,
                                  retrieval_threshold=0.01):
        entities_to_test = self.get_random_persons_others_sentences(is_person=is_person,
                                                                    person_nb=person_nb,
                                                                    min_sent=min_sent,
                                                                    max_sent=max_sent)
        if is_person:
            main_dict = self.persons
            side_dict = self.others
        else:
            main_dict = self.others
            side_dict = self.persons

        p_tot = r_tot = f1_tot = 0

        for mid, sentences in entities_to_test.items():
            type2score = {}
            current_entity = main_dict[mid][0]
            for sentence in sentences:
                e1, relation, e2 = sentence

                if e1 in main_dict:
                    e1 = main_dict[e1][0]
                else:
                    e1 = side_dict[e1][0]

                if e2 in main_dict:
                    e2 = main_dict[e2][0]
                else:
                    e2 = side_dict[e2][0]

                word_bio = tag_triple(e1, relation, e2)

                # [('Trump', [('type1', score1), ('type2', score2)])]
                entity_typescore = self.model.predict_scores_given_bio(word_bio, retrieval_threshold)

                for entity, type_score in entity_typescore:
                    if entity == current_entity:
                        for type, score in type_score:
                            if type in type2score:
                                type2score[type] = type2score[type] + score
                            else:
                                type2score[type] = score

            if len(type2score) < 1:
                print('Empty type2score: {} - mid: {}'.format(type2score, mid))
                continue

            max_score = max(type2score.values())
            for k in type2score:
                type2score[k] /= max_score
            predicted_types = sorted(type2score.items(), key=lambda tup: tup[1], reverse=True)
            predicted_types = [i[0] for i in predicted_types if i[1] >= threshold]

            correct_types = main_dict[mid][1]

            p, r, f1 = calculate_difference(predicted_types, correct_types)
            p_tot += p
            r_tot += r
            f1_tot += f1
            print('{}\t{}\tPrecision:\t{}\tRecall:\t{}\tF1-score:\t{}'.format(mid, len(sentences), p, r, f1))

        norm_value = len(entities_to_test)
        p = p_tot / norm_value
        r = r_tot / norm_value
        f1 = f1_tot / norm_value

        print('Precision:\t{}\nRecall:\t{}\nF1-score:\t{}\n'.format(p, r, f1))

        return p, r, f1

    def get_random_persons_others_sentences(self, is_person=True, person_nb=100, min_sent=5, max_sent=250):
        print('Getting sentences for {} {}'.format(person_nb, 'person' if is_person else 'others'))

        entities_dict = self.persons if is_person else self.others
        entities_to_test = {}

        with open(path_settings.SENTENCES_LECTOR_FILE) as f:
            curr_e1 = None
            for line in f:
                e1, relation, e2, count = line.rstrip().split('\t')

                if e1 in entities_dict:
                    if curr_e1 != e1:
                        if curr_e1 in entities_to_test:
                            if len(entities_to_test[curr_e1]) < min_sent or len(entities_to_test[curr_e1]) > max_sent:
                                del entities_to_test[curr_e1]

                        if len(entities_to_test) == person_nb and person_nb != 0:
                            return entities_to_test

                        curr_e1 = e1
                        entities_to_test[e1] = []

                    if e2 in self.persons or e2 in self.others:
                        entities_to_test[e1].append((e1, relation, e2))

            print('Getting entities from second entity.')
            curr_e2 = None
            f.seek(0)
            for line in f:
                e1, relation, e2, count = line.rstrip().split('\t')

                if e2 in entities_dict:
                    if curr_e2 != e2:
                        if curr_e2 in entities_to_test:
                            if len(entities_to_test[curr_e2]) < min_sent or len(entities_to_test[curr_e2]) > max_sent:
                                del entities_to_test[curr_e2]

                        if len(entities_to_test) == person_nb:
                            return entities_to_test

                        curr_e2 = e2
                        entities_to_test[e2] = []

                    if e2 in self.persons or e2 in self.others:
                        entities_to_test[e2].append((e1, relation, e2))

        if person_nb == 0:
            entity_nb = 0
            sentence_nb = 0

            for entity in entities_to_test:
                entity_nb += 1
                sentence_nb += len(entities_to_test[entity])

            print('Calculated {} entities for a total of {} sentences'.format(entity_nb, sentence_nb))

            return entities_to_test
        else:
            raise ValueError('Not enough entities!')

    def calculate_stats(self):
        sentence_nb = 0
        e1_absent_sentence_nb = 0
        e2_absent_sentence_nb = 0
        e1_absent_list = []
        e2_absent_list = []

        with open(path_settings.SENTENCES_LECTOR_FILE) as f:
            for line in f:
                sentence_nb += 1

                e1, relation, e2, count = line.rstrip().split('\t')

                if e1 in self.persons:
                    name_e1, types_e1 = self.persons[e1]
                    # print('{} in person as {}'.format(e1, name_e1))

                    if e1 not in self.persons_stats:
                        self.persons_stats[e1] = {}

                    for type_e1 in types_e1:
                        if type_e1 in self.persons_stats[e1]:
                            self.persons_stats[e1][type_e1] += 1
                        else:
                            self.persons_stats[e1][type_e1] = 1

                elif e1 in self.others:
                    name_e1, types_e1 = self.others[e1]
                    # print('{} in others'.format(e1, name_e1))

                    if e1 not in self.others_stats:
                        self.others_stats[e1] = {}

                    for type_e1 in types_e1:
                        if type_e1 in self.others_stats[e1]:
                            self.others_stats[e1][type_e1] += 1
                        else:
                            self.others_stats[e1][type_e1] = 1

                else:
                    e1_absent_sentence_nb += 1
                    if e1 not in e1_absent_list:
                        e1_absent_list.append(e1)
                        # print('e1 mid {} NOT present!'.format(e1))
                        # raise ValueError('mid {} NOT present!'.format(e1))

                if e2 in self.persons:
                    name_e2, types_e2 = self.persons[e2]
                    # print('{} in person as {}'.format(e2, name_e2))

                    if e2 not in self.persons_stats:
                        self.persons_stats[e2] = {}

                    for type_e2 in types_e2:
                        if type_e2 in self.persons_stats[e2]:
                            self.persons_stats[e2][type_e2] += 1
                        else:
                            self.persons_stats[e2][type_e2] = 1

                elif e2 in self.others:
                    name_e2, types_e2 = self.others[e2]
                    # print('{} in others'.format(e2, name_e2))

                    if e2 not in self.others_stats:
                        self.others_stats[e2] = {}

                    for type_e2 in types_e2:
                        if type_e2 in self.others_stats[e2]:
                            self.others_stats[e2][type_e2] += 1
                        else:
                            self.others_stats[e2][type_e2] = 1

                else:
                    e2_absent_sentence_nb += 1
                    if e2 not in e2_absent_list:
                        e2_absent_list.append(e2)
                        # print('e2 mid {} NOT present!'.format(e2))

            self.print_stats()

            print('Sentences (total: {}) with entity absent - e1: {} - e2: {}'
                  .format(sentence_nb, e1_absent_sentence_nb, e2_absent_sentence_nb))
            print('MIDs found in sentences absent in "persons" or "others" - e1: {} - e2: {}'
                  .format(len(e1_absent_list), len(e2_absent_list)))

    def print_stats(self):
        print('PERSONS TYPES:')
        print_generic_stats(self.persons_stats)

        print('OTHERS TYPES:')
        print_generic_stats(self.others_stats)

        print('------------------------------')
        print('Persons in person_lector: {}\nOthers in others_lector: {}'.format(len(self.persons), len(self.others)))


def print_generic_stats(stats_dict):
    for entity in stats_dict:
        entity_types = []
        for type in stats_dict[entity]:
            entity_types.append(type)
        print('{} - {}'.format(entity, entity_types))


def tag_triple(e1, relation, e2):
    word_bio = []

    for ix, token in enumerate(tokenizer.tokenize_in_words(e1)):
        if ix == 0:
            word_bio.append((token, 'B'))
        else:
            word_bio.append((token, 'I'))

    for token in tokenizer.tokenize_in_words(relation):
        word_bio.append((token, 'O'))

    for ix, token in enumerate(tokenizer.tokenize_in_words(e2)):
        if ix == 0:
            word_bio.append((token, 'B'))
        else:
            word_bio.append((token, 'I'))

    return word_bio
