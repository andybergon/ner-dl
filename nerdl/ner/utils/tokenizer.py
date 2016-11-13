import string

from nltk.tokenize import word_tokenize, sent_tokenize


def tokenize_word(text):
    return word_tokenize(text)


# N.B. Remember that tokenization isn't a fully reversible process. Information is lost in tokenization.
def untokenize_word(tokens):
    return "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip()


def untokenize_word_custom(tokens):
    result = ' '.join(tokens)
    result = result.replace(' , ', ',')
    result = result.replace(' .', '.')
    result = result.replace(' !', '!')
    result = result.replace(' ?', '?')
    result = result.replace(' : ', ': ')
    result = result.replace(' \'', '\'')
    return result


def tokenize_sentence(text):
    return sent_tokenize(text)
