class SentencesExtractor:
    def __init__(self):
        pass

    def extract_sentences(self, dataset_fp, sentences_fp, sentence_nb=0, print_every=100000):
        current_sentence = 0
        sentence_words = []
        with open(dataset_fp) as f_in, open(sentences_fp, 'w') as f_out:
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
                        print('Extracted Sentence #{}/{}'.format(current_sentence, sentence_nb))

                    if current_sentence == sentence_nb:
                        return

            print('Extracted ALL #{} Sentences'.format(current_sentence))
