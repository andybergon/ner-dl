import string.punctuation
from nltk.tokenize import word_tokenize


def word_tokenize(text):
    return word_tokenize(text)


def word_untokenize(tokens):
    return "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip()


def word_untokenize_2(tokens):
    result = ' '.join(tokens)
    result = result.replace(' , ', ',')
    result = result.replace(' .', '.')
    result = result.replace(' !', '!')
    result = result.replace(' ?', '?')
    result = result.replace(' : ', ': ')
    result = result.replace(' \'', '\'')
    return result


def sentence_tokenize(text):
    return sentence_tokenize(text)
