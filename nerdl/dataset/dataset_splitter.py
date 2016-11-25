import random

random.seed(0)


def split_dataset(dataset_fp, train_fp, test_fp, test_perc=0.2, sentence_nb=0, print_every=100000):
    current_sentence = 0
    tagged_words = []

    with open(dataset_fp) as in_f, open(train_fp, 'w') as train_f, open(test_fp, 'w') as test_f:
        for line in in_f:
            if line != '\n':
                word, tag = line.rstrip().split('\t')
                tagged_words.append((word, tag))
            else:
                if random.uniform(0, 1) > test_perc:
                    to_write_f = train_f
                else:
                    to_write_f = test_f

                for word_and_tag in tagged_words:
                    word = word_and_tag[0]
                    tag = word_and_tag[1]
                    line_to_write = '{}\t{}\n'.format(word, tag)
                    to_write_f.write(line_to_write)

                to_write_f.write('\n')
                tagged_words = []
                current_sentence += 1

                if current_sentence % print_every == 0:
                    print('Sentence #{}/{}'.format(current_sentence, sentence_nb))

                if current_sentence == sentence_nb:
                    print('Splitted #{}/{} sentences.'.format(current_sentence, sentence_nb))
                    return

    print('Splitted ALL #{}/{} sentences.'.format(current_sentence, sentence_nb))
