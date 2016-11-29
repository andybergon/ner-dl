import random

random.seed(0)  # for debugging


class DatasetSplitterShortener:
    def __init__(self, dataset_fp, train_fp, test_fp):
        self.dataset_fp = dataset_fp
        self.train_fp = train_fp
        self.test_fp = test_fp

    def split_and_shorten(self, min_len=15, max_len=50, test_perc=0.2, sentence_nb=0, print_every=100000):
        curr_sentence_nb = 0
        processed_sentences_nb = 0
        tagged_words = []

        with open(self.dataset_fp) as in_f, open(self.train_fp, 'w') as train_f, open(self.test_fp, 'w') as test_f:
            for line in in_f:
                if line != '\n':
                    word, tag = line.rstrip().split('\t')
                    tagged_words.append((word, tag))
                else:
                    curr_sentence_nb += 1
                    sentence_len = len(tagged_words)
                    if min_len <= sentence_len <= max_len:
                        if random.uniform(0, 1) > test_perc:
                            to_write_f = train_f
                        else:
                            to_write_f = test_f

                        for word, tag in tagged_words:
                            to_write_f.write('{}\t{}\n'.format(word, tag))
                        to_write_f.write('\n')

                        processed_sentences_nb += 1

                        if print_every != 0 and processed_sentences_nb % print_every == 0:
                            print('Writing Sentence #{}/{}, {} processed.'
                                  .format(processed_sentences_nb, sentence_nb, curr_sentence_nb))

                        if processed_sentences_nb == sentence_nb:
                            print('Wrote #{}/{} sentences, {} processed.'
                                  .format(processed_sentences_nb, sentence_nb, curr_sentence_nb))
                            return

                    tagged_words = []  # reset current sentence in any case

        print('Wrote ALL sentences. (#{}/{}, {} processed)'
              .format(processed_sentences_nb, sentence_nb, curr_sentence_nb))
