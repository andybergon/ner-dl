import numpy as np

from settings import path_settings
from settings import settings


class Tag2VecReader:
    def __init__(self):
        self.tag2vec_map = {}  # contains both 'tag-vec' and 'vec-tag'
        self.nb_classes = 0

        self.class_list = settings.TAG2VEC_CLASS_LIST

        if len(self.class_list) == 0 or not self.class_list:
            print('Calculating output labels...')
            training_filepath = path_settings.TRAINING_FILE
            self.training_filepath = training_filepath

            self.calculate_output_labels()
        else:
            self.populate_tag_vector_map(self.class_list)

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

            # tags.append('NIL')

            for tag in tags:
                one_hot_vec = np.zeros(len(tags), dtype=np.int32)
                one_hot_vec[tag_class_id] = 1
                self.tag2vec_map[tag] = tuple(one_hot_vec)
                self.tag2vec_map[tuple(one_hot_vec)] = tag
                tag_class_id += 1

            self.nb_classes = tag_class_id + 1

    def populate_tag_vector_map(self, class_list):
        tag_class_id = 0

        for tag in class_list:
            one_hot_vec = np.zeros(len(class_list), dtype=np.int32)
            one_hot_vec[tag_class_id] = 1
            self.tag2vec_map[tag] = tuple(one_hot_vec)
            self.tag2vec_map[tuple(one_hot_vec)] = tag
            tag_class_id += 1

        self.nb_classes = tag_class_id

    def encode_tag(self, tag):
        return self.tag2vec_map[tag]

    def encode_tags_list(self, tags):
        if len(tags) <= 1:
            tags_vector = self.tag2vec_map[tags[0]]  # avoid useless calculations, not strictly needed
        else:
            tags_vector = self.encode_multiple_tags(tags)

        return tags_vector

    def encode_multiple_tags(self, tags):
        vector = [0] * self.nb_classes

        for tag in tags:
            current_vector = list(self.tag2vec_map[tag])
            vector = map(sum, zip(vector, current_vector))

        return vector

    def decode_prediction_max(self, pred_seq):
        pred_tags = []

        for class_prs in pred_seq:
            class_vec = np.zeros(self.nb_classes, dtype=np.int32)
            class_vec[np.argmax(class_prs)] = 1

            if tuple(class_vec.tolist()) in self.tag2vec_map:
                pred_tags.append(self.tag2vec_map[tuple(class_vec.tolist())])

        return pred_tags

    def decode_prediction_percentage(self, pred_seq, cutoff_perc=0.95):
        pass  # TODO
