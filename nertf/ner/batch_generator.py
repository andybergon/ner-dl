import numpy as np


class BatchGenerator:
    def __init__(self, word2vec_reader, training_filepath, test_filepath, class_list, max_sentence_len):
        """
        :param class_list: List of classes, NIL included. If empty, it's calculated from training data
        """

        self.word2vec_reader = word2vec_reader
        self.training_filepath = training_filepath
        self.test_filepath = test_filepath
        self.max_sentence_len = max_sentence_len

        self.tag_vector_map = {}
        self.nb_classes = 0

        if len(class_list) == 0 or not class_list:
            print('Calculating output labels...')
            self.calculate_output_labels()
        else:
            self.populate_tag_vector_map(class_list)

    def calculate_output_labels(self):
        with open(self.training_filepath, 'rt') as f:
            sentence_num = 0
            tag_class_id = 0
            tags = []

            for line in f:
                line = line.strip()

                if line == '\n':  # blank line
                    sentence_num += 1

                    if sentence_num % 100000 == 0:
                        print('Loaded {} training sentences'.format(sentence_num))

                    continue

                try:
                    word, tag = line.split('\t')
                except ValueError as e:
                    print(e.message)
                    print('Error at sentence #{}.\n Line: {}'.format(sentence_num, line))

                if tag not in tags:
                    tags.append(tag)

            tags.append('NIL')

            for tag in tags:
                one_hot_vec = np.zeros(len(tags), dtype=np.int32)
                one_hot_vec[tag_class_id] = 1
                self.tag_vector_map[tag] = tuple(one_hot_vec)
                self.tag_vector_map[tuple(one_hot_vec)] = tag
                tag_class_id += 1

            self.nb_classes = tag_class_id + 1

    def populate_tag_vector_map(self, class_list):
        tag_class_id = 0

        for tag in class_list:
            one_hot_vec = np.zeros(len(class_list), dtype=np.int32)
            one_hot_vec[tag_class_id] = 1
            self.tag_vector_map[tag] = tuple(one_hot_vec)
            self.tag_vector_map[tuple(one_hot_vec)] = tag
            tag_class_id += 1

        self.nb_classes = tag_class_id

    def generate_training_batch(self):
        return self.generate_batch(self.training_filepath)

    def generate_test_batch(self):
        return self.generate_batch(self.test_filepath)

    def generate_multiple_training_batch(self, batch_size):
        return self.generate_batch_multiple(self.training_filepath, batch_size)

    def generate_multiple_test_batch(self, batch_size):
        return self.generate_batch_multiple(self.test_filepath, batch_size)

    def generate_batch(self, filepath):
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
                        print(
                            'Error at sentence #{}.\nError message: {}.\nLine: {}.'.format(sentence_num, e.message,
                                                                                           line))

            f.close()

    def convert_tagged_sentence_to_vectors(self, word_tag_list):
        w2v_reader = self.word2vec_reader
        sentence_words_vec, sentence_tags_vec = [], []

        for word, tags in word_tag_list:
            if word in self.word2vec_reader.word_to_ix_map:
                word_vec = w2v_reader.wordvecs[w2v_reader.word_to_ix_map[word]]
            else:
                new_wv = 2 * np.random.randn(w2v_reader.n_features) - 1  # sample from normal distribution
                norm_const = np.linalg.norm(new_wv)
                new_wv /= norm_const
                w2v_reader.word_to_ix_map[word] = w2v_reader.wordvecs.shape[0]
                w2v_reader.wordvecs = np.vstack((w2v_reader.wordvecs, new_wv))
                word_vec = new_wv

            sentence_words_vec.append(word_vec)
            if len(tags) <= 1:
                tags_vector = self.tag_vector_map[tags[0]]
            else:
                tags_vector = self.tags_to_vector(tags)
            sentence_tags_vec.append(list(tags_vector))

        # Pad the sequences for missing entries to make them all the same length
        nil_X = np.zeros(w2v_reader.n_features)
        nil_Y = np.array(self.tag_vector_map['NIL'])
        pad_length = self.max_sentence_len - len(sentence_words_vec)
        X = (pad_length * [nil_X]) + sentence_words_vec
        Y = (pad_length * [nil_Y]) + sentence_tags_vec

        X = np.array([X])
        Y = np.array([Y])

        return X, Y

    def tags_to_vector(self, tags):
        vector = [0] * self.nb_classes
        for tag in tags:
            current_vector = list(self.tag_vector_map[tag])
            vector = map(sum, zip(vector, current_vector))

        return vector

    # TODO: merge w/ generate_batch
    def generate_batch_multiple(self, filepath, batch_size=1):
        sentence_num = 0
        nb_sentences_curr_batch = 0
        sentences_curr_batch = []
        word_tag_list = []

        while 1:
            f = open(filepath)
            for line in f:
                if line == '\n':  # blank line
                    sentence_num += 1
                    nb_sentences_curr_batch += 1

                    sentences_curr_batch.append(word_tag_list)
                    word_tag_list = []

                    if nb_sentences_curr_batch == batch_size:
                        X, Y = self.convert_multiple_tagged_sentence_to_vectors(sentences_curr_batch)
                        nb_sentences_curr_batch = 0
                        sentences_curr_batch = []
                        yield (X, Y)
                else:
                    try:
                        word, tag = line.replace('\n', '').split('\t')
                        word_tag_list.append((word, tag))
                    except ValueError as e:
                        print(
                            'Error at sentence #{}.\nError message: {}.\nLine: {}.'.format(sentence_num,
                                                                                           e.message,
                                                                                           line))

            f.close()

    def convert_multiple_tagged_sentence_to_vectors(self, sentences_curr_batch):
        w2v_reader = self.word2vec_reader
        sentence_words_vec, sentence_tags_vec = [], []
        X, Y = [], []

        nil_X = np.zeros(w2v_reader.n_features)
        nil_Y = np.array(self.tag_vector_map['NIL'])

        for sentence in sentences_curr_batch:
            for word, tag in sentence:
                if word in self.word2vec_reader.word_to_ix_map:
                    word_vec = w2v_reader.wordvecs[w2v_reader.word_to_ix_map[word]]
                else:
                    new_wv = 2 * np.random.randn(w2v_reader.n_features) - 1  # sample from normal distribution
                    norm_const = np.linalg.norm(new_wv)
                    new_wv /= norm_const
                    w2v_reader.word_to_ix_map[word] = w2v_reader.wordvecs.shape[0]
                    w2v_reader.wordvecs = np.vstack((w2v_reader.wordvecs, new_wv))
                    word_vec = new_wv

                sentence_words_vec.append(word_vec)
                sentence_tags_vec.append(list(self.tag_vector_map[tag]))

            # Pad the sequences for missing entries to make them all the same length
            pad_length = self.max_sentence_len - len(sentence_words_vec)
            XX = (pad_length * [nil_X]) + sentence_words_vec
            YY = (pad_length * [nil_Y]) + sentence_tags_vec

            X.append(XX)
            Y.append(YY)

        X = np.array(X)
        Y = np.array(Y)

        return X, Y
