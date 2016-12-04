from nerdl.ner.iterators.sentences_iterator import SentencesIterator


class DatasetIterator(SentencesIterator):
    def __init__(self, file_fp):
        SentencesIterator.__init__(self, file_fp)

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
            return word_tag
        else:
            raise ValueError
