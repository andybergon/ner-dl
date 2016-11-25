import random

from nerdl.dataset.cw.midnames_manager import MidnamesManager
from nerdl.dataset.too_long_exception import TooLongException
from nerdl.ner.utils import tokenizer
from settings import path_settings

random.seed(0)


class CWDatasetGenerator:
    def __init__(self):
        self.midnames_manager = MidnamesManager()

    def create_dataset(self,
                       sentence_nb=0,
                       skip_sentences_longer_than=80,
                       remove_duplicate_lines=True,
                       remove_duplicate_lines_after_sub=True):
        """
        :param sentence_nb: Number of sentences needed. If 0, process all corpus file.
        :param skip_sentences_longer_than:
        :param remove_duplicate_lines:
        :param remove_duplicate_lines_after_sub:
        :return:
        """

        corpus_fp = path_settings.CW_CORPUS_FILE
        dataset_fp = path_settings.CW_DATASET_CW_TAGS_FILE

        current_line_nb = 0
        effective_sentences_nb = 0
        duplicate_lines_num = 0
        duplicate_lines_after_sub = 0
        mid_not_found = 0
        too_long_sentence = 0

        prev_phrase = ''
        prev_phrase_after_sub = ''

        with open(dataset_fp, 'w+') as dataset_f, open(corpus_fp, 'r') as corpus_f:
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
                for word_and_tag in tagged_words:
                    word = word_and_tag[0]
                    tag = word_and_tag[1]
                    line_to_write = '{}\t{}\n'.format(word, tag)
                    dataset_f.write(line_to_write)

                dataset_f.write('\n')

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
                            entity_mid, entity_name, entity_types = self.get_all_entity_properties_by_id(mid)

                            entity_name_list = tokenizer.tokenize_in_words(entity_name)

                            for i, entity_name_part in enumerate(entity_name_list):
                                if i == 0:
                                    entity_tag = ''.join(['B-', ','.join(entity_types)])
                                else:
                                    entity_tag = ''.join(['I-', ','.join(entity_types)])

                                tagged_words.append((entity_name_part, entity_tag))

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

    # {m.01000036} => ('m.01000036', 'God Has Given Me' [music.single,music.recording,common.topic])
    def get_all_entity_properties_by_id(self, entity_id):
        try:
            row = self.midnames_manager.get_row_by_id(entity_id)
        except ValueError:
            raise

        entity_id, entity_name, entity_types = row.replace('\n', '').split('\t')
        entity_types = entity_types.split(',')
        return entity_id, entity_name, entity_types
