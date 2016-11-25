from settings import path_settings


class FigerConverter:
    def __init__(self, tagger):
        self.tagger = tagger

    def convert_dataset(self, sentence_nb=0, print_every=1000):
        current_sentence = 0
        with open(path_settings.FIGER_DATASET_CW_TAGS_FILE) as f_in, \
                open(path_settings.FIGER_DATASET_FG_TAGS_FILE, 'w') as f_out:
            for line in f_in:
                if line != '\n':
                    word, tags = line.rstrip().split('\t')
                    if tags != 'O':
                        tags = tags.replace('/', '', 1).replace(',/', ',').replace('/', '.').upper()
                        tags = tags.split(',')
                        tags = self.tagger.tag(tags)
                    f_out.write('{}\t{}\n'.format(word, tags))
                else:
                    f_out.write('\n')
                    current_sentence += 1

                    if current_sentence % print_every == 0:
                        print('Converted sentence #{}/{}'.format(current_sentence, sentence_nb))

                    if current_sentence == sentence_nb:
                        return

    def extract_sentences(self, sentence_nb=0, print_every=1000):
        current_sentence = 0
        sentence_words = []
        with open(path_settings.FIGER_DATASET_CW_TAGS_FILE) as f_in, \
                open(path_settings.FIGER_SENTENCES_FILE, 'w') as f_out:
            for line in f_in:
                if line != '\n':
                    word, tags = line.rstrip().split('\t')
                    sentence_words.append(word)
                else:
                    sentence_words = ' '.join(sentence_words)
                    f_out.write('{}\n'.format(sentence_words))
                    sentence_words = []
                    current_sentence += 1

                    if current_sentence % print_every == 0:
                        print('Converted sentence #{}/{}'.format(current_sentence, sentence_nb))

                    if current_sentence == sentence_nb:
                        return
