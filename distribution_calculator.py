import os
import pickle
import json
import read_training as rt

corpus_file = os.path.join(os.path.dirname(__file__), 'data/cw_1_sentences.tsv')
# corpus_file = os.path.join(os.path.dirname(__file__), 'data/cw_1_sentences_example.tsv')
# corpus_file = os.path.join(os.path.dirname(__file__), 'data/cw_1_sentences_1k.tsv')
mid_name_file = os.path.join(os.path.dirname(__file__), 'data/mid_name_types.tsv')
checkpoint_file = os.path.join(os.path.dirname(__file__), 'data/checkpoint_type_distribution.tsv')


def count_types():
    types = {}
    line_number = 0
    missing_id_occ = 0
    open(checkpoint_file, 'w').close()  # clean checkpoint file
    with open(corpus_file, "rb") as f:
        for line in f:
            line_number += 1

            if line_number % 10000 == 0:
                with open(checkpoint_file, "a") as cf:
                    cf.write(str(line_number))
                    cf.write('\n')
                    sorted_types_list = sort_dict_by_value_ascending_into_list(types)
                    cf.write(str(sorted_types_list))
                    cf.write('\n')

            _, phrase = line.split('\t')

            try:
                types_in_phrase = rt.get_types_in_phrase(phrase)
                types = rt.merge_two_dicts(types, types_in_phrase)
            except ValueError as e:
                missing_id_occ += 1
                print('entity id missing: ' + e.message)
                print('# phrases skipped: ' + str(missing_id_occ))
                continue

    return sort_dict_by_value_ascending_into_list(types)


def sort_dict_by_value_ascending_into_list(dict_to_sort):
    # return sorted(dict_to_sort, key=key=operator.itemgetter(1), reverse=True)  # non mostra numeri
    return sorted(dict_to_sort.items(), key=lambda x:x[1], reverse=True)


def dict_to_string(dict_to_convert):
    return str(dict_to_convert)


def string_to_dict(json_to_convert):
    return eval(json_to_convert)


def dict_to_json_string(dict_to_convert):
    return json.dumps(dict_to_convert)


def json_string_to_dict(json_to_convert):
    return json.loads(json_to_convert)


def read_dict_from_file():
    with open(checkpoint_file, 'rb') as handle:
        return pickle.loads(handle.read())


def write_dict_to_file(dict_to_write):
    with open(checkpoint_file, 'wb') as handle:
        pickle.dump(dict_to_write, handle)


def read_dict_as_json_from_file():
    with open(checkpoint_file, 'r') as f:
        try:
            data = json.load(f)
        except ValueError:  # if the file is empty
            data = {}
        return data


def write_dict_as_json_to_file(dict_to_write):
    with open(checkpoint_file, 'w') as f:
        json.dump(dict_to_write, f)


print count_types()
