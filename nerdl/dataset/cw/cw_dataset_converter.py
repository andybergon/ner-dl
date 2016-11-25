from settings import path_settings


class CWDatasetConverter:
    def __init__(self, tagger, output_fp=path_settings.CW_DATASET_FG_TAGS_FILE):
        self.tagger = tagger
        self.output_fp = output_fp

    def convert_dataset(self, sentence_nb=0, print_every=100000):
        current_sentence = 0
        with open(path_settings.CW_DATASET_CW_TAGS_FILE) as f_in, open(self.output_fp, 'w') as f_out:
            for line in f_in:
                if line != '\n':
                    word, tags = line.rstrip().split('\t')
                    if tags != 'O':
                        if len(tags.split('-')) == 2:  # contains BIO tags
                            bio, tags = tags.split('-')
                            tags = tags.replace('/', '', 1).replace(',/', ',').replace('/', '.').upper()
                            tags = tags.split(',')
                            tags = self.tagger.tag(tags)
                            tags = bio + '-' + tags
                        else:
                            tags = tags.replace('/', '', 1).replace(',/', ',').replace('/', '.').upper()
                            tags = tags.split(',')
                            tags = self.tagger.tag(tags)

                    f_out.write('{}\t{}\n'.format(word, tags))
                else:
                    f_out.write('\n')
                    current_sentence += 1

                    if current_sentence % print_every == 0:
                        print('Converted Sentence #{}/{}'.format(current_sentence, sentence_nb))

                    if current_sentence == sentence_nb:
                        return
