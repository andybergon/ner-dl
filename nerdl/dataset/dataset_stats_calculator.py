from __future__ import division


class DatasetStatsCalculator:
    def __init__(self, dataset_fp):
        self.dataset_fp = dataset_fp

    def calculate_type_distribution(self, sentence_nb=0, print_every=1000000):
        type2occ = {}
        current_sentence = 0

        with open(self.dataset_fp) as ds_f:
            for line in ds_f:
                if line != '\n':
                    word, tag = line.rstrip().split('\t')
                    if tag != 'O':
                        bi, tag = tag.split('-')
                        types = tag.split(',')
                        for type in types:
                            if type in type2occ:
                                type2occ[type] += 1
                            else:
                                type2occ[type] = 1
                else:
                    current_sentence += 1

                    if print_every != 0 and current_sentence % print_every == 0:
                        print_sentences_types_stats(type2occ)

                    if current_sentence == sentence_nb:
                        print_sentences_types_stats(type2occ)
                        return

            print_sentences_types_stats(type2occ)

        return type2occ

    def calculate_sentence_length(self, sentence_nb=0, print_every=1000000):
        len2occ = {}
        current_sentence = 0
        current_sentence_length = 0

        with open(self.dataset_fp) as ds_f:
            for line in ds_f:
                if line != '\n':
                    current_sentence_length += 1
                else:
                    if current_sentence_length in len2occ:
                        len2occ[current_sentence_length] += 1
                    else:
                        len2occ[current_sentence_length] = 1

                    current_sentence += 1
                    current_sentence_length = 0

                    if print_every != 0 and current_sentence % print_every == 0:
                        print_sentences_length_stats(len2occ)

                    if current_sentence == sentence_nb:
                        print_sentences_length_stats(len2occ)
                        return

            print_sentences_length_stats(len2occ)

        return len2occ


def print_sentences_types_stats(type2occ):
    occ_sum = 0

    type2occ['common.topic'] = 0  # reset, always present

    for ix in type2occ:
        occ_sum += type2occ[ix]

    cum_perc = 0
    top_types = sorted(type2occ.items(), key=lambda x: x[1], reverse=True)[:50]
    for k, v in top_types:
        perc = v / occ_sum
        cum_perc += perc
        print('{}\t{}\t{:.3%}\t{:.3%}'.format(k, v, perc, cum_perc))

    print('Total Types Tags: {}\nUnique Tags: {}'.format(occ_sum, len(type2occ)))


def print_sentences_length_stats(len2occ):
    occ_sum = 0

    for ix in len2occ:
        occ_sum += len2occ[ix]

    print('Total Sentences Analyzed: {}'.format(occ_sum))

    cum_perc = 0
    for k, v in sorted(len2occ.items()):
        perc = v / occ_sum
        cum_perc += perc
        print('{}\t{}\t{:.3%}\t{:.3%}'.format(k, v, perc, cum_perc))
