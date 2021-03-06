import random
import re
from collections import Counter
from itertools import islice

import nerdl.dataset.midnames

from nerdl.dataset.too_long_exception import TooLongException
from nerdl.ner.utils import tokenizer
from settings import path_settings

random.seed(0)


class TestTrainingGenerator:
    def __init__(self, tagger):
        self.tagger = tagger

    def create_training_and_test(self,
                                 sentence_nb=0,
                                 skip_sentences_longer_than=80,
                                 remove_duplicate_lines=True,
                                 remove_duplicate_lines_after_sub=True,
                                 test_percentage=0.2):
        """
        :param sentence_nb: Number of sentences needed. If 0, process all corpus file.
        :param skip_sentences_longer_than:
        :param remove_duplicate_lines:
        :param remove_duplicate_lines_after_sub:
        :param test_percentage:
        :return:
        """

        corpus_fp = path_settings.CW_CORPUS_FILE
        training_fp = path_settings.TRAINING_FILE
        test_fp = path_settings.TEST_FILE

        current_line_nb = 0
        effective_sentences_nb = 0
        duplicate_lines_num = 0
        duplicate_lines_after_sub = 0
        mid_not_found = 0
        too_long_sentence = 0

        prev_phrase = ''
        prev_phrase_after_sub = ''

        with open(training_fp, 'wt') as training_f, open(test_fp, 'wt') as test_f, open(corpus_fp, 'rt') as corpus_f:
            for line in corpus_f:
                current_line_nb += 1
                if current_line_nb % 1000 == 0:
                    print('Processing line #{} - Effective sentences: #{}/{}'
                          .format(current_line_nb, effective_sentences_nb, sentence_nb))

                _, phrase = line.rstrip().split('\t')

                if remove_duplicate_lines and (phrase == prev_phrase):
                    duplicate_lines_num += 1
                    continue
                prev_phrase = phrase

                try:
                    tagged_words, phrase_after_sub = self.tag_phrase(phrase, skip_sentences_longer_than)
                except TooLongException:
                    too_long_sentence += 1
                    continue
                except ValueError:
                    mid_not_found += 1
                    continue

                # don't use (prev_phrase = phrase), already updated
                if remove_duplicate_lines_after_sub and (phrase_after_sub == prev_phrase_after_sub):
                    duplicate_lines_after_sub += 1
                    continue
                prev_phrase_after_sub = phrase_after_sub

                # WRITE SENTENCE TO FILE
                if random.uniform(0, 1) > test_percentage:
                    to_write_f = training_f
                else:
                    to_write_f = test_f

                for word_and_tag in tagged_words:
                    word = word_and_tag[0]
                    tag = word_and_tag[1]
                    line_to_write = '{}\t{}\n'.format(word, tag)
                    to_write_f.write(line_to_write)

                to_write_f.write('\n')

                effective_sentences_nb += 1

                if effective_sentences_nb == sentence_nb and sentence_nb != 0:
                    print('Wrote all {} sentences.'.format(sentence_nb))
                    break

            if sentence_nb == 0:  # EOF reached
                print('Corpus file ended. Wrote #{} effective sentences after #{} lines.'
                      .format(effective_sentences_nb, current_line_nb))

        print('Skipped Sentences - Mid not found: {}/{} {}'
              .format(mid_not_found, effective_sentences_nb, mid_not_found / (mid_not_found + effective_sentences_nb)))
        print('Skipped Sentences - Duplicate: {}/{} {}'
              .format(duplicate_lines_num, effective_sentences_nb,
                      duplicate_lines_num / (duplicate_lines_num + effective_sentences_nb)))
        print('Skipped Sentences - Duplicate (only after substitution): {}/{}'
              .format(duplicate_lines_after_sub, effective_sentences_nb,
                      duplicate_lines_after_sub / (duplicate_lines_after_sub + effective_sentences_nb)))
        print('Skipped Sentences - Too Long: {}/{}'
              .format(too_long_sentence, effective_sentences_nb,
                      too_long_sentence / (too_long_sentence + effective_sentences_nb)))

    def tag_phrase(self, phrase, skip_sentences_longer_than):
        tagged_words = []
        skip_token_mid = False  # for double continue on token found
        skip_token_end = False  # for double continue on token found

        words = tokenizer.tokenize_in_words(phrase)
        words_len = len(words)

        for idx, word in enumerate(words):

            if skip_token_mid:
                skip_token_mid = False
                continue

            if skip_token_end:
                skip_token_end = False
                continue

            if word == '{':
                if idx + 1 < words_len and words[idx + 1].startswith('m.'):
                    mid = words[idx + 1].split(':')[0]
                    if idx + 2 < words_len and words[idx + 2] == '}':

                        try:
                            entity_mid, entity_name, entity_types = get_all_entity_properties_by_id(mid)
                            entity_tag = self.tagger.tag(entity_types)
                            entity_tag = ','.join(entity_tag)

                            entity_name_list = tokenizer.tokenize_in_words(entity_name)

                            for entity_part in entity_name_list:
                                tagged_words.append((entity_part, entity_tag))

                            word_to_replace = '{' + words[idx + 1] + '}'
                            phrase.replace(word_to_replace, entity_name)

                        except ValueError:
                            raise

                        skip_token_mid = True
                        skip_token_end = True

                    else:  # rare case
                        tagged_words.append((word, 'O'))
                else:
                    tagged_words.append((word, 'O'))
            else:
                tagged_words.append((word, 'O'))

        tagged_words_len = len(tagged_words)
        if tagged_words_len > skip_sentences_longer_than:
            raise TooLongException('Too long sentence. Found {} tokens.'.format(tagged_words_len))

        return tagged_words, phrase


# support functions
def substitute_midnames(lines_num=0, remove_duplicate_lines=True, remove_duplicate_lines_after_sub=True):
    corpus_file = path_settings.CW_CORPUS_FILE
    replaced_file = path_settings.REPLACED_CORPUS_FILE

    duplicate_lines_num = 0
    duplicate_lines_after_sub = 0
    mid_not_found = 0
    prev_phrase = ''
    prev_phrase_after_sub = ''

    with open(replaced_file, 'wt') as fout:
        with open(corpus_file, 'rt') as fin:

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
                    phrase_after_sub = substitute_midnames_in_phrase(phrase)
                    # don't use (prev_phrase = phrase) because already updated
                    if remove_duplicate_lines_after_sub and (phrase_after_sub == prev_phrase_after_sub):
                        duplicate_lines_after_sub += 1
                        continue
                    prev_phrase_after_sub = phrase_after_sub

                    fout.write(phrase_after_sub)
                except ValueError:
                    mid_not_found += 1
                    continue

    print('mid not found sentences: {}/{}'.format(mid_not_found, lines_num))
    print('duplicate sentences: {}/{}'.format(duplicate_lines_num, lines_num))
    print('duplicate only after substitution sentences: {}/{}'.format(duplicate_lines_after_sub, lines_num))


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


# {m.01000036} => ('m.01000036', 'God Has Given Me' [music.single,music.recording,common.topic])
def get_all_entity_properties_by_id(entity_id):
    try:
        row = nerdl.dataset.midnames.get_row_by_id(entity_id)
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


def count_sentence_length(filepath):
    sentence_num = 0
    words, tags = [], []
    lengths = []

    with open(filepath, 'r') as f:
        for line in f:
            if line == '\n':
                sentence_num += 1
                length = len(words)
                # lengths.append(length)

                if length > 80:
                    print('Length: {}.\nSentence: {}\n'.format(length, words))

                words, tags = [], []
            else:
                word, tag = line.replace('\n', '').split('\t')
                words.append(word)
                tags.append(tag)
    return lengths
