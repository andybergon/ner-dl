def tagged_sentence_to_entities(word_tag_score, word_bio, threshold):
    """

    :param word_tag_score: [('Trump', [('person', 1), ('politician', 0.75)]), [('is', [('O', 1)])], ...]
    :param word_bio: [('Trump', 'B'), ('is', 'O'), ...]
    :param threshold: 0.1
    :return: entity_tags: [('Trump', ['person', 'politician'], ('United States', ['location']))
    """
    entity_tags = []
    current_entity = []

    for wts, wb in zip(word_tag_score, word_bio):
        wts_word, wts_tag_score_list = wts
        wb_word, wb_bio = wb

        if wts_word == wb_word:
            if wb_bio == 'O':
                if len(current_entity) > 0:
                    e_t = calculate_types(current_entity, threshold)
                    entity_tags.append(e_t)
                    current_entity = []
            elif wb_bio == 'B':
                if len(current_entity) > 0:
                    e_t = calculate_types(current_entity, threshold)
                    entity_tags.append(e_t)
                current_entity = [(wts_word, wts_tag_score_list)]
            elif wb_bio == 'I':
                current_entity.append((wts_word, wts_tag_score_list))
            else:
                raise ValueError('Tag BIO "{}" incorrect!'.format(wb_bio))
        else:
            print('Tokenizing Error!')
            raise ValueError('Tokenizing Error!')

    if len(current_entity) > 0:
        e_t = calculate_types(current_entity, threshold)
        entity_tags.append(e_t)

    return entity_tags


def calculate_types(current_entity, threshold):
    """

    :param current_entity: [('United', [('location', 0.7)('a', 0.05)]), ('States', [('place', 0.2)])]
    :param threshold: e.g. 0.1
    :return: ('United States', ['location', 'place'])
    """
    types = []

    words, tags_scores = zip(*current_entity)
    words = ' '.join(words)

    for tag_scores in tags_scores:
        for tag, score in tag_scores:
            if score >= threshold:
                if tag not in types:
                    if tag != 'O' and tag != 'NIL':
                        types.append(tag)

    return words, types
