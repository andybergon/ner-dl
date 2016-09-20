import re
from itertools import islice

# corpus_file = 'cw_1_sentences.tsv'
corpus_file = 'cw_1_sentences_example.tsv'
mid_name_file = 'mid_name_types.tsv'
# mid_name_file = 'mid_name_types_example.tsv'
new_corpus_file = corpus_file.split('.tsv')[0] + '_replaced.tsv'


def substitute_midnames(corpus_file, new_corpus_file):
    with open(new_corpus_file, "wt") as fout:
        with open(corpus_file, "rt") as fin:
            head = list(islice(fin,1))
            for line in head:
                warc, phrase = line.split('\t')
                fout.write(substitute_midname_in_phrase(phrase))


def substitute_midnames_partial(corpus_file, new_corpus_file):
    with open(new_corpus_file, "wt") as fout:
        with open(corpus_file, "rt") as fin:
            head = list(islice(fin,1))
            for line in head:
                warc, phrase = line.split('\t')
                fout.write(substitute_midname_in_phrase(phrase))


# TODO optimize scanning midname file one time
def substitute_midname_in_phrase(phrase):
    print 'original: ' + phrase
    m = re.findall('{.*?}', phrase)
    for match in m:
        match_name = get_entity_name_by_token(match)
        phrase = phrase.replace(match, match_name)
    print 'new: ' + phrase
    return phrase


def get_entity_name_by_token(token):
    id = get_id_by_token(token)
    return get_entity_name_by_id(id)


def get_id_by_token(token):
    r = re.compile('m\.(.*?):')
    m = r.search(token)
    if m:
        id = m.group(0).replace(':', '')
        return id


def get_entity_name_by_id(id):
    with open(mid_name_file, "rt") as f:
        for line in f:
            entity_id, entity_name, entity_type = line.split('\t')
            if line.startswith(id):
                entity_id, entity_name, entity_type = line.split('\t')
                return entity_name


substitute_midnames(corpus_file, new_corpus_file)
# print get_id_by_token('{m.03cd5dk:45037:45040}')
# print search_midname('m.01000036')