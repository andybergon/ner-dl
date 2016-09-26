import os
import read_training as rt

# corpus_file = os.path.join(os.path.dirname(__file__), 'data/cw_1_sentences.tsv')
corpus_file = os.path.join(os.path.dirname(__file__), 'data/cw_1_sentences_example.tsv')
mid_name_file = os.path.join(os.path.dirname(__file__), 'data/mid_name_types.tsv')


def count_types():
    types = {}
    with open(corpus_file, "rt") as f:
        for line in f:
            warc, phrase = line.split('\t')
            print('phrase: ', phrase)
            types_in_phrase = rt.get_types_in_phrase(phrase)
            print('types in phrase: ', types_in_phrase)
            types = rt.merge_two_dicts(types, types_in_phrase)
    return types
    # return sorted(types, key=d.get, reverse=True)
