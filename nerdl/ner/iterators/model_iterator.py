from nerdl.ner.iterators.sentences_iterator import SentencesIterator


class ModelIterator(SentencesIterator):
    def __init__(self, model, file_fp):
        self.model = model

        self.file_fp = file_fp
        self.is_file_open = None
        self.file_f = self.open_file()

    def open_file(self):
        self.is_file_open = True
        return open(self.file_fp, 'r')

    def close_file(self):
        print('EOF reached. Closing {} ModelIterator file.'.format(self.file_fp))
        self.is_file_open = False
        self.file_f.close()

    def count_sentences(self):
        count = 0
        with open(self.file_fp, 'r') as f:
            for line in f:
                if line == '\n' or line == '\t\n':
                    count += 1
        return count

    def next(self):
        word_tag = []

        line = self.file_f.readline()

        while line != '' and line != '\n' and line != '\t\n':
            word_tag.append((line.rstrip().split('\t')))
            line = self.file_f.readline()

        if line == '':
            self.close_file()
            return word_tag  # can be omitted
        elif line == '\n' or line == '\t\n':
            tokenized_sentence = [i[0] for i in word_tag]
            word_tag_prediction = self.model.predict_tokenized_sentence(tokenized_sentence)
            return word_tag_prediction
        else:
            raise ValueError
