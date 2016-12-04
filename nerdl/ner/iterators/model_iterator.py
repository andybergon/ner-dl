from nerdl.ner.iterators.sentences_iterator import SentencesIterator


class ModelIterator(SentencesIterator):
    def __init__(self, file_fp, model):
        SentencesIterator.__init__(self, file_fp)

        self.model = model

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
