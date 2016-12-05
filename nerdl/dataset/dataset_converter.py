class DatasetConverter:
    def __init__(self, dataset_fp, dataset_converted_fp, tagger):
        self.dataset_fp = dataset_fp
        self.dataset_converted_fp = dataset_converted_fp
        self.tagger = tagger

    def convert(self, sentence_nb=0, print_every=100000):
        processed_sentences_nb = 0
        tagged_words = []

        with open(self.dataset_fp) as in_f, open(self.dataset_converted_fp, 'w') as out_f:
            for line in in_f:
                if line != '\n':
                    word, tag = line.rstrip().split('\t')
                    tagged_words.append((word, tag))
                else:
                    for word, tag in tagged_words:
                        if 'B-' in tag or 'I-' in tag:
                            bio, tag = tag.split('-', 1)
                            tags = tag.split(',')
                            converted_tag = self.tagger.tag(tags)
                            converted_tag = ','.join(converted_tag)
                            tag = bio + '-' + converted_tag
                        else:
                            tags = tag.split(',')
                            converted_tag = self.tagger.tag(tags)
                            converted_tag = ','.join(converted_tag)
                            tag = converted_tag

                        out_f.write('{}\t{}\n'.format(word, tag))

                    out_f.write('\n')

                    processed_sentences_nb += 1

                    if print_every != 0 and processed_sentences_nb % print_every == 0:
                        print('Writing Sentence #{}/{}.'.format(processed_sentences_nb, sentence_nb))

                    if processed_sentences_nb == sentence_nb:
                        print('Wrote #{}/{} sentences.'.format(processed_sentences_nb, sentence_nb))
                        return

                    tagged_words = []  # reset current sentence in any case

        print('Wrote ALL sentences. (#{}/{})'.format(processed_sentences_nb, sentence_nb))
