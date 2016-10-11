import numpy as np
import pandas as pd

from keras.preprocessing import sequence


class Word2VecReader:
    def __init__(self, word2vec_filepath=None, annotated_filepath=None):

        self.DEFAULT_N_FEATURES = 300
        self.DEFAULT_N_CLASSES = 6  # [LOC, PER, ORG, MISC, O, NIL]
        self.DEFAULT_MAX_SEQ_LENGTH = 29

        self.wordvecs = None
        self.word_to_ix_map = {}

        self.n_features = 0
        self.n_tag_classes = 0
        self.max_sentence_len = 0

        self.n_sentences_all = 0
        self.tag_vector_map = {}

        self.all_X = []
        self.all_Y = []

        if word2vec_filepath and annotated_filepath:
            self.read_and_parse_data(word2vec_filepath, annotated_filepath)

    def read_and_parse_data(self, word2vec_filepath, annotated_filepath, skip_unknown_words=False):

        # skiprows=1 to skip first line
        self.wordvecs = pd.read_table(word2vec_filepath, sep=' ', header=None, skiprows=1)
        # <class 'pandas.core.frame.DataFrame'>
        # print(self.wordvecs.shape)

        self.word_to_ix_map = {}
        for ix, row in self.wordvecs.iterrows():
            self.word_to_ix_map[row[0]] = ix

        # axis=1 for columns
        self.wordvecs = self.wordvecs.drop(self.wordvecs.columns[0], axis=1).as_matrix()
        # <type 'numpy.ndarray'>
        print('Shape: {}'.format(self.wordvecs.shape))

        self.n_features = len(self.wordvecs[0])
        # print(self.n_features)

        # Read in training data and create map to match tag classes to tags and create tag to class index map
        with open(annotated_filepath, 'r') as f:
            self.n_tag_classes = self.DEFAULT_N_CLASSES
            self.tag_vector_map = {}
            sentence_num = 0
            tag_class_id = 0
            tagged_sentences = []
            words_current_sentence = []
            tags_current_sentence = []

            for line in f:
                line = line.strip()
                if not line:  # blank line
                    sentence_num += 1
                    if sentence_num % 100000 == 0:
                        print('Loaded {} training sentences'.format(sentence_num))

                    tagged_sentences.append((tuple(words_current_sentence), tuple(tags_current_sentence)))
                    words_current_sentence = []
                    tags_current_sentence = []
                    continue

                try:
                    word, tag = line.split('\t')
                except ValueError as e:
                    print(e.message)
                    print('error at sentence #{}'.format(sentence_num))
                    print(line)

                words_current_sentence.append(word)
                tags_current_sentence.append(tag)

                if tag not in self.tag_vector_map:
                    one_hot_vec = np.zeros(self.DEFAULT_N_CLASSES, dtype=np.int32)
                    one_hot_vec[tag_class_id] = 1
                    self.tag_vector_map[tag] = tuple(one_hot_vec)
                    self.tag_vector_map[tuple(one_hot_vec)] = tag
                    tag_class_id += 1

        # Add NIL class
        one_hot_vec = np.zeros(self.DEFAULT_N_CLASSES, dtype=np.int32)
        one_hot_vec[tag_class_id] = 1
        self.tag_vector_map['NIL'] = tuple(one_hot_vec)
        self.tag_vector_map[tuple(one_hot_vec)] = 'NIL'

        self.n_sentences_all = len(tagged_sentences)
        print('total training sentences: {}'.format(self.n_sentences_all))

        # Build the data as required for training
        self.max_sentence_len = 0
        for seq in tagged_sentences:
            if len(seq[0]) > self.max_sentence_len:
                self.max_sentence_len = len(seq[0])
        print('max length in training sentences: {}'.format(self.max_sentence_len))

        self.all_X, self.all_Y = [], []
        unk_words = []
        for words, tags in tagged_sentences:
            elem_wordvecs, elem_tags = [], []

            for ix in xrange(len(words)):
                w = words[ix]
                t = tags[ix]

                if w in self.word_to_ix_map:
                    elem_wordvecs.append(self.wordvecs[self.word_to_ix_map[w]])
                    elem_tags.append(list(self.tag_vector_map[t]))
                # Ignore unknown words, removing from dataset
                elif skip_unknown_words:
                    unk_words.append(w)
                    continue
                # Randomly select a 300-elem vector for unknown words
                else:
                    unk_words.append(w)
                    new_wv = 2 * np.random.randn(self.n_features) - 1  # sample from normal distn
                    norm_const = np.linalg.norm(new_wv)
                    new_wv /= norm_const
                    self.word_to_ix_map[w] = self.wordvecs.shape[0]
                    self.wordvecs = np.vstack((self.wordvecs, new_wv))
                    elem_wordvecs.append(new_wv)
                    elem_tags.append(list(self.tag_vector_map[t]))

            # Pad the sequences for missing entries to make them all the same length
            nil_X = np.zeros(self.n_features)
            nil_Y = np.array(self.tag_vector_map['NIL'])
            pad_length = self.max_sentence_len - len(elem_wordvecs)
            self.all_X.append((pad_length * [nil_X]) + elem_wordvecs)
            self.all_Y.append((pad_length * [nil_Y]) + elem_tags)

        self.all_X = np.array(self.all_X)
        self.all_Y = np.array(self.all_Y)

        # print "UNKNOWN WORDS " + str(unk_words)
        # print "UNK WORD COUNT " + str(len(unk_words))
        # print "TOTAL WORDS " + str(self.wordvecs.shape[0])

        return self.all_X, self.all_Y

    def get_data(self):
        return self.all_X, self.all_Y

    def encode_sentence(self, sentence, skip_unknown_words=False):
        X = []
        outer_X = []

        for word in sentence:

            if word in self.word_to_ix_map:
                X.append(self.wordvecs[self.word_to_ix_map[word]])
            elif skip_unknown_words:
                continue
            else:
                new_wv = 2 * np.random.randn(self.n_features) - 1  # sample from normal distribution
                norm_const = np.linalg.norm(new_wv)
                new_wv /= norm_const
                X.append(new_wv)

        outer_X.append(X)

        return sequence.pad_sequences(outer_X, maxlen=self.max_sentence_len, dtype=np.float64)

    def decode_prediction_sequence(self, pred_seq):
        pred_tags = []

        for class_prs in pred_seq:
            class_vec = np.zeros(self.n_tag_classes, dtype=np.int32)
            class_vec[np.argmax(class_prs)] = 1

            if tuple(class_vec.tolist()) in self.tag_vector_map:
                pred_tags.append(self.tag_vector_map[tuple(class_vec.tolist())])

        return pred_tags
