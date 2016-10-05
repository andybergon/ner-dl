import re
from collections import Counter
from itertools import islice

import midnames as mi


def create_training_from_dataset(corpus_file, training_file, lines_num=0, remove_duplicate_lines=True):
    duplicate_lines_num = 0
    mid_not_found = 0
    prev_phrase = ''

    with open(training_file, 'wt') as fout:
        with open(corpus_file, 'rt') as fin:

            fout.write('-DOCSTART-	O\n')
            fout.write('\n')

            if lines_num <= 0:
                lines_num = sum(1 for _ in open(corpus_file))

            for i in range(1, lines_num):
                if i % 1000 == 0:
                    print('# {}/{}'.format(i, lines_num))

                line = fin.readline()
                _, phrase = line.replace('\n', '').split('\t')

                if remove_duplicate_lines and (phrase == prev_phrase):
                    duplicate_lines_num += 1
                    continue
                prev_phrase = phrase

                try:
                    tagged_words = tag_phrase(phrase)
                except ValueError:
                    mid_not_found += 1
                    continue

                for word_and_tag in tagged_words:
                    word = word_and_tag[0]
                    tag = word_and_tag[1]
                    line_to_write = '{}\t{}\n'.format(word, tag)
                    fout.write(line_to_write)

                fout.write('\n')

    print('duplicate sentences: {}/{}'.format(duplicate_lines_num, lines_num))
    print('mid not found sentences: {}/{}'.format(mid_not_found, lines_num))


def tag_phrase(phrase):
    tagged_words = []
    words = phrase.split(' ')  # TODO: use tokenizer

    for word in words:
        if is_entity(word):
            mid = get_id_by_token(word)

            try:
                _, entity_name, entity_types = get_all_entity_properties_by_id(mid)
                entity_tag = get_tag_from_types(entity_types)

                # TODO: use BIO/BILOU NER tags
                for entity_part in entity_name.split(' '):  # TODO: use tokenizer
                    tagged_words.append((entity_part, entity_tag))

            except ValueError:
                raise

        else:
            if word != '':  # double whitespace that remains after split()
                tagged_words.append((word, 'O'))

    return tagged_words


# TODO: oppure usare regex?
def is_entity(word):
    return word.startswith('{m.')


def get_tag_from_types(entity_types):
    entity_domain = get_types_domain(entity_types)

    if 'location' in entity_domain:
        return 'LOC'
    elif 'organization' in entity_domain:
        return 'ORG'
    elif 'people' in entity_domain:
        return 'PER'
    else:
        return 'MISC'


def get_types_domain(entity_types):
    entity_domains = set()

    for entity_type in entity_types:
        entity_domain = entity_type.split('.')[0]
        entity_domains.add(entity_domain)

    return entity_domains


def substitute_midnames(corpus_file, new_corpus_file, lines_num=0, remove_duplicate_lines=True):
    duplicate_lines_num = 0
    mid_not_found = 0
    prev_phrase = ''

    with open(new_corpus_file, 'wt') as fout:
        with open(corpus_file, 'rt') as fin:

            if lines_num <= 0:
                lines_num = sum(1 for _ in open(corpus_file))

            # head = list(islice(fin, lines_num))
            # for line in head:
            for i in range(1, lines_num):
                if i % 1000 == 0:
                    print('# {}/{}'.format(i, lines_num))

                line = fin.readline()
                warc, phrase = line.split('\t')

                if remove_duplicate_lines and (phrase == prev_phrase):
                    duplicate_lines_num += 1
                    continue

                prev_phrase = phrase

                try:
                    fout.write(substitute_midnames_in_phrase(phrase))
                except ValueError:
                    mid_not_found += 1
                    continue

    print('duplicate sentences: {}/{}'.format(duplicate_lines_num, lines_num))
    print('mid not found sentences: {}/{}'.format(mid_not_found, lines_num))


def substitute_midnames_in_phrase(phrase):
    m = get_tokens_in_phrase(phrase)
    for match in m:
        match_name = get_entity_name_by_token(match)
        phrase = phrase.replace(match, match_name)
    return phrase


def get_tokens_in_phrase(phrase):
    return re.findall('{[m].*?}', phrase)


def get_entity_name_by_token(token):
    entity_id = get_id_by_token(token)
    return get_entity_name_by_id(entity_id)


# {m.01000036} => God Has Given Me
def get_entity_name_by_id(entity_id):
    return get_all_entity_properties_by_id(entity_id)[1]


def get_all_entity_properties_by_token(token):
    entity_id = get_id_by_token(token)
    return get_all_entity_properties_by_id(entity_id)


def get_id_by_token(token):
    r = re.compile('m\.(.*?):')
    m = r.search(token)
    if m:
        entity_id = m.group(0).replace(':', '')
        return entity_id


# {m.01000036} => music.single,music.recording,common.topic
def get_entity_types_by_id(entity_id):
    return get_all_entity_properties_by_id(entity_id)[2]


# {m.01000036} => ('m.01000036', 'God Has Given Me' 'music.single,music.recording,common.topic')
def get_all_entity_properties_by_id(entity_id):
    try:
        row = mi.get_row_by_id(entity_id)
    except ValueError:
        raise

    entity_id, entity_name, entity_types = row.replace('\n', '').split('\t')
    entity_types = entity_types.split(',')
    return entity_id, entity_name, entity_types


# {m.01000036} => {m.01000036|God Has Given Me|music.single,music.recording,common.topic}
def get_all_entity_properties_formatted_by_id(entity_id):
    entity_id, entity_name, entity_type = get_all_entity_properties_by_id(entity_id)
    return "{" + entity_id + "|" + entity_name + "|" + entity_type + "}"


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


def count_entities_in_phrase(phrase):
    return len(get_tokens_in_phrase(phrase))


def sample_dataset(corpus_file, new_corpus_file, lines_num):
    with open(new_corpus_file, 'wt') as fout:
        with open(corpus_file, 'rt') as fin:
            head = list(islice(fin, lines_num))
            for line in head:
                fout.write(line)
