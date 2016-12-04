from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree


def get_entities(text):
    """

    :param text: 'Brooklyn is in New York'
    :return: ['Brooklyn', 'New York']
    """
    return get_continuous_chunks(text)


def get_bio_tags(tokenized_sentence):
    """

    :param tokenized_sentence: ['Trump', 'is', ..., 'United', 'States']
    :return: [('Trump', 'B'), ('is', 'O'), ..., ('United', 'B'), ('States', 'I')]
    """
    word_tag = []
    chunked = ne_chunk(pos_tag(tokenized_sentence))

    for i in chunked:
        if type(i) == Tree:
            for position, token_pos in enumerate(i.leaves()):
                if position == 0:
                    word_tag.append((token_pos[0], 'B'))
                else:
                    word_tag.append((token_pos[0], 'I'))
        else:
            word_tag.append((i[0], 'O'))

    return word_tag


def get_continuous_chunks(text):
    """

    :param text: 'Brooklyn is in New York'
    :return: ['Brooklyn', 'New York']
    """
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue
    return continuous_chunk


if __name__ == '__main__':
    tok_sent = word_tokenize('Trump is the president of the United States')
    word_bio = get_bio_tags(tok_sent)
    print(word_bio)
