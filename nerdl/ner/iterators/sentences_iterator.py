class SentencesIterator:
    def __init__(self, file_fp):
        self.file_fp = file_fp
        self.is_file_open = None
        self.file_f = self.open_file()

    def open_file(self):
        self.is_file_open = True
        return open(self.file_fp, 'r')

    def close_file(self):
        print('EOF reached. Closing {} SentencesIterator file.'.format(self.file_fp))
        self.is_file_open = False
        self.file_f.close()

    def return_to_file_beginning(self):
        self.file_f.seek(0)

    def count_sentences(self):
        count = 0
        with open(self.file_fp, 'r') as f:
            for line in f:
                if line == '\n' or line == '\t\n':
                    count += 1
        return count

    def next(self):
        pass
