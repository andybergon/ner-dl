import numpy as np

from settings import path_settings
from settings import settings


class BatchGenerator:
    def __init__(self, word2vec_reader, tag2vec_reader):
        self.word2vec_reader = word2vec_reader
        self.tag2vec_reader = tag2vec_reader

        self.training_fp = path_settings.TRAINING_FILE
        self.test_fp = path_settings.TEST_FILE
        self.training_checkpoint_fp = path_settings.TRAINING_CHECKPOINT_FILE
        self.test_checkpoint_fp = path_settings.TEST_CHECKPOINT_FILE

        self.max_sentence_len = settings.MAX_SENTENCE_LEN  # to calculate padding length

    def generate_training_batch(self, batch_size=1, resume_gen=False):
        return self.generate_batch(self.training_fp, self.training_checkpoint_fp, batch_size, resume_gen)

    def generate_test_batch(self, batch_size=1, resume_gen=False):
        return self.generate_batch(self.test_fp, self.test_checkpoint_fp, batch_size, resume_gen)

    def generate_batch(self, filepath, checkpoint_fp, batch_size, resume_gen, cp_frequency=1000):
        sentence_num = 0
        first_loop_end = False
        sentences_curr_batch = []
        word_tag_list = []

        while 1:
            with open(filepath) as f, open(checkpoint_fp, 'r+') as c_f:

                initial_position = c_f.readline()
                if not initial_position or not resume_gen or first_loop_end:
                    initial_position = 0

                f.seek(initial_position)

                for line in f:  # starts from seek?
                    if line == '\n':  # blank line
                        sentence_num += 1

                        if sentence_num % cp_frequency == 0:
                            c_f.seek(0)
                            c_f.truncate()
                            current_position = f.tell()
                            c_f.write(current_position)

                        sentences_curr_batch.append(word_tag_list)
                        word_tag_list = []

                        if len(sentences_curr_batch) == batch_size:
                            X, Y = self.convert_multiple_tagged_sentence_to_vectors(sentences_curr_batch)
                            sentences_curr_batch = []
                            yield (X, Y)
                    else:
                        try:
                            word, tag = line.replace('\n', '').split('\t')
                            word_tag_list.append((word, tag))
                        except ValueError as e:
                            print('Error at sentence #{}.\nError message: {}.\nLine: {}.'
                                  .format(sentence_num, e.message, line))

            first_loop_end = True

    def convert_multiple_tagged_sentence_to_vectors(self, sentences_curr_batch):
        w2v_r = self.word2vec_reader
        t2v_r = self.tag2vec_reader

        sentence_words_vec, sentence_tags_vec = [], []
        X, Y = [], []

        nil_X = np.zeros(w2v_r.n_features)
        nil_Y = np.array(t2v_r.encode_tag('NIL'))

        for sentence in sentences_curr_batch:
            for word, tags in sentence:
                word_vec = w2v_r.encode_word(word)
                sentence_words_vec.append(word_vec)

                tag_vector = t2v_r.encode_tags_list(tags)
                sentence_tags_vec.append(list(tag_vector))

            # Pad the sequences for missing entries to make them all the same length
            pad_length = self.max_sentence_len - len(sentence_words_vec)
            XX = (pad_length * [nil_X]) + sentence_words_vec
            YY = (pad_length * [nil_Y]) + sentence_tags_vec

            X.append(XX)
            Y.append(YY)

        X = np.array(X)
        Y = np.array(Y)

        return X, Y

    # OLD

    # def generate_training_batch(self):
    #     return self.generate_batch(self.training_filepath)
    #
    # def generate_test_batch(self):
    #     return self.generate_batch(self.test_filepath)

    def generate_batch_single(self, filepath):
        sentence_num = 0
        word_tags_list = []

        while 1:
            f = open(filepath)
            for line in f:

                if line == '\n':  # blank line
                    sentence_num += 1

                    # print('yielding sentence #{}\t{}'.format(sentence_num, word_tag_list))

                    X, Y = self.convert_tagged_sentence_to_vectors(word_tags_list)

                    # if X.shape[1] != 80:
                    #     print('X Shape: {}\t{}'.format(X.shape, len(word_tag_list)))

                    word_tags_list = []

                    yield (X, Y)
                else:
                    try:
                        word, tags = line.replace('\n', '').split('\t')
                        tags = tags.split(',')
                        word_tags_list.append((word, tags))
                    except ValueError as e:
                        print('Error at sentence #{}.\nError message: {}.\nLine: {}.'
                              .format(sentence_num, e.message, line))

            f.close()

    def convert_tagged_sentence_to_vectors(self, word_tag_list):
        w2v_r = self.word2vec_reader
        t2v_r = self.tag2vec_reader

        sentence_words_vec, sentence_tags_vec = [], []

        for word, tags in word_tag_list:
            word_vec = w2v_r.encode_word(word)
            sentence_words_vec.append(word_vec)

            tag_vector = t2v_r.encode_tags_list(tags)
            sentence_tags_vec.append(list(tag_vector))

        # Pad the sequences for missing entries to make them all the same length
        nil_X = np.zeros(w2v_r.n_features)
        nil_Y = np.array(t2v_r.encode_tag('NIL'))
        pad_length = self.max_sentence_len - len(sentence_words_vec)
        X = (pad_length * [nil_X]) + sentence_words_vec
        Y = (pad_length * [nil_Y]) + sentence_tags_vec

        X = np.array([X])
        Y = np.array([Y])

        return X, Y
