import os
import read_training as rt

# corpus_file = os.path.join(os.path.dirname(__file__), 'data/cw_1_sentences.tsv')
corpus_file = os.path.join(os.path.dirname(__file__), 'data/cw_1_sentences_example.tsv')
mid_name_file = os.path.join(os.path.dirname(__file__), 'data/mid_name_types.tsv')
checkpoint_file = os.path.join(os.path.dirname(__file__), 'data/checkpoint_type_distribution.tsv')


def count_types():
    types = {}
    line_number = 0
    missing_id_occ = 0
    with open(corpus_file, "rt") as f:
        for line in f:
            line_number += 1
            if line_number % 10000
            warc, phrase = line.split('\t')
            try:
                types_in_phrase = rt.get_types_in_phrase(phrase)
                types = rt.merge_two_dicts(types, types_in_phrase)
            except ValueError as e:
                missing_id_occ += 1
                print('entity id missing: ' + e.message)
                print('# phrases skipped: ' + str(missing_id_occ))
                continue
    return types
    # return sorted(types, key=d.get, reverse=True)


print count_types()
