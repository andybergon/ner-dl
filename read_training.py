import os
import re
from collections import Counter
from itertools import islice
import midnames_index as mi

# corpus_file = os.path.join(os.path.dirname(__file__), 'data/cw_1_sentences.tsv')
corpus_file = os.path.join(os.path.dirname(__file__), 'data/cw_1_sentences_example.tsv')
mid_name_file = os.path.join(os.path.dirname(__file__), 'data/mid_name_types.tsv')
new_corpus_file = corpus_file.split('.tsv')[0] + '_replaced.tsv'


def substitute_midnames():
    with open(new_corpus_file, "wt") as fout:
        with open(corpus_file, "rt") as fin:
            for line in fin:
                warc, phrase = line.split('\t')
                fout.write(substitute_midname_in_phrase(phrase))


def substitute_midnames_partial():
    with open(new_corpus_file, "wt") as fout:
        with open(corpus_file, "rt") as fin:
            head = list(islice(fin, 1))
            for line in head:
                warc, phrase = line.split('\t')
                fout.write(substitute_midname_in_phrase(phrase))


def substitute_midname_in_phrase(phrase):
    print 'old: ' + phrase
    m = re.findall('{.*?}', phrase)
    for match in m:
        match_name = get_entity_name_by_token(match)
        phrase = phrase.replace(match, match_name)
    print 'new: ' + phrase
    return phrase


def get_entity_name_by_token(token):
    entity_id = get_id_by_token(token)
    return get_entity_name_by_id(entity_id)


def get_all_entity_properties_by_token(token):
    entity_id = get_id_by_token(token)
    return get_all_entity_properties_by_id(entity_id)


def get_id_by_token(token):
    r = re.compile('m\.(.*?):')
    m = r.search(token)
    if m:
        entity_id = m.group(0).replace(':', '')
        return entity_id


# {m.01000036} => {m.01000036|God Has Given Me|music.single,music.recording,common.topic}
def get_all_entity_properties_formatted_by_id(entity_id):
    entity_id, entity_name, entity_type = get_all_entity_properties_by_id(entity_id)
    return "{" + entity_id + "|" + entity_name + "|" + entity_type + "}"


# {m.01000036} => ('m.01000036', 'God Has Given Me' 'music.single,music.recording,common.topic')
def get_all_entity_properties_by_id(entity_id):
    try:
        row = mi.get_row_by_id(entity_id)
    except ValueError:
        raise
    entity_id, entity_name, entity_type = row.replace('\n', '').split('\t')
    return entity_id, entity_name, entity_type


# {m.01000036} => God Has Given Me
def get_entity_name_by_id(entity_id):
    return get_all_entity_properties_by_id(entity_id)[1]


# {m.01000036} => music.single,music.recording,common.topic
def get_entity_types_by_id(entity_id):
    return get_all_entity_properties_by_id(entity_id)[2]


# {m.01000036} => {God Has Given Me}
def get_entity_name_by_id_not_opt(entity_id):
    with open(mid_name_file, "rt") as f:
        for line in f:
            if line.startswith(entity_id):
                entity_id, entity_name, entity_type = line.split('\t')
                return entity_name


# {m.01000036} => {m.01000036|God Has Given Me|music.single,music.recording,common.topic}
def get_all_entity_properties_by_id_not_opt(entity_id):
    with open(mid_name_file, "rt") as f:
        for line in f:
            if line.startswith(entity_id + "\t"):
                entity_id, entity_name, entity_type = line.replace('\n', '').split('\t')
                return "{" + entity_id + "|" + entity_name + "|" + entity_type + "}"


def get_tokens_in_phrase(phrase):
    return re.findall('{[m].*?}', phrase)


def get_types_in_phrase(phrase):
    types_in_phrase = {}
    matches = get_tokens_in_phrase(phrase)

    for token in matches:
        entity_id = get_id_by_token(token)

        try:
            types_string = get_all_entity_properties_by_id(entity_id)[2]
        except ValueError:
            raise

        entity_types = types_string.split(',')
        types_in_phrase = merge_two_dicts(types_in_phrase, entity_types)
    return types_in_phrase


def merge_two_dicts(a, b):
    return dict(Counter(a) + Counter(b))


# IN MEMORY (needs 3GB+ RAM)
def substitute_midnames_in_memory():
    midnames = load_midnames_dictionary(mid_name_file)

    with open(new_corpus_file, "wt") as fout:
        with open(corpus_file, "rt") as fin:
            for line in fin:
                warc, phrase = line.split('\t')
                new_phrase = substitute_midname_in_phrase_in_memory(phrase, midnames)
                fout.write(new_phrase)


# 45M entities - 44789550
def load_midnames_dictionary(midnames_file):
    midnames = {}
    line_number = 1
    with open(midnames_file, "rt") as f:
        for line in f:
            entity_id, entity_name, entity_type = line.split('\t')
            midnames[entity_id] = (entity_name, entity_type)
            if line_number % 100000 == 0:
                print str(line_number / 1000000.0) + 'M'
            line_number += 1
    return midnames


def substitute_midname_in_phrase_in_memory(phrase, midnames):
    print 'original: ' + phrase
    m = re.findall('{.*?}', phrase)
    for match in m:
        match_name = midnames[match][0]
        phrase = phrase.replace(match, match_name)
    print 'new: ' + phrase
    return phrase
