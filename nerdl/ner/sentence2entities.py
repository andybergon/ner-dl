class Sentence2Entities:
    def __init__(self, is_bio=True, auto_detect=False, tagger=None):
        self.is_bio = is_bio
        self.auto_detect = auto_detect
        self.tagger = tagger

    def convert_to_entities(self, word_tag):
        if self.auto_detect:
            is_bio = check_tags(word_tag)
            self.is_bio = is_bio

        if self.is_bio:
            return self.convert_bio_to_entities(word_tag)
        else:
            return self.convert_not_bio_to_entities(word_tag)

    def convert_not_bio_to_entities(self, word_tag):
        """

        :param word_tag: [('Barack', ['/person', '/person/politician']), ('Obama', ['/person', '/person/politician']]
        :return: [('Barack Obama', ['/person', '/person/politician'])]
        """
        entity_and_type = []
        current_entity = []
        is_prev_tag_entity = False

        for word, tag in word_tag:
            if self.tagger:
                tag = self.tagger.tag_string(tag)

            if tag != ['O']:
                if not is_prev_tag_entity:  # first word of entity
                    is_prev_tag_entity = True
                    current_entity.append((word, tag))
                else:  # middle word of entity
                    current_entity.append((word, tag))
                    # TODO: don't recognize 2 types near as different. check if types different, no one in common
            else:
                if is_prev_tag_entity:
                    is_prev_tag_entity = False

                    words, types = zip(*current_entity)
                    entity_word = ' '.join(words)
                    entity_types = calculate_types(types)

                    entity_and_type.append((entity_word, entity_types))
                    current_entity = []

        if len(current_entity) > 0:  # entity at end of sentence
            words, types = zip(*current_entity)
            entity_word = ' '.join(words)
            entity_types = calculate_types(types)

            entity_and_type.append((entity_word, entity_types))

        return entity_and_type

    # TODO: check edge cases
    def convert_bio_to_entities(self, word_tag):
        """

        :param word_tag: [('Barack', 'B-/person'), ('Obama', 'I-/person')]
        :return:
        """
        entity_and_type = []
        current_entity = []

        for word, tag in word_tag:
            if self.tagger:
                tag = self.tagger.tag_string(tag)

            if tag != 'O':
                bio, tag = tag.split('-')
                if bio == 'B':
                    if len(current_entity) == 0:
                        current_entity = [(word, tag)]  # can append instead
                    else:  # B tag after B/I tag
                        words, types = zip(*current_entity)
                        entity_word = ' '.join(words)
                        entity_types = calculate_types_bio(types)

                        entity_and_type.append((entity_word, entity_types))

                        current_entity = [(word, tag)]  # can append instead

                elif bio == 'I':
                    current_entity.append((word, tag))
                else:
                    raise ValueError('Tag BIO "{}" incorrect!'.format(bio))
            else:
                if len(current_entity) > 0:
                    words, types = zip(*current_entity)
                    entity_word = ' '.join(words)
                    entity_types = calculate_types_bio(types)

                    entity_and_type.append((entity_word, entity_types))

                    current_entity = []

        if len(current_entity) > 0:
            words, types = zip(*current_entity)
            entity_word = ' '.join(words)
            entity_types = calculate_types_bio(types)

            entity_and_type.append((entity_word, entity_types))

        return entity_and_type


# TODO: more strategies
def calculate_types(types):
    """

    :param types: list of lists. e.g. [[A, B], [B, C], [B]]
    :return:
    """
    final_types = []

    for word_types in types:
        for word_type in word_types:
            if word_type not in final_types:
                final_types.append(word_type)

    return final_types


def calculate_types_bio(types):
    # TODO: check that all types are equal
    return types[0].split(',')


def check_tags(word_tag):
    types = [i[1] for i in word_tag]

    for type in types:
        if 'B-' in type or 'I-' in type:
            return True

    return False
