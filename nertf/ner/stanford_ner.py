from nltk.tag.stanford import StanfordNERTagger

import settings
import tokenizer


class StanfordNERModel:
    def __init__(self, nb_classes=4):
        if nb_classes == 4:
            classifier_file = settings.STANFORD_NER_CLASSIFIER_4C
        elif nb_classes == 3:
            classifier_file = settings.STANFORD_NER_CLASSIFIER_3C
        else:
            raise ValueError('Number of classes not supported')

        self.classifier = StanfordNERTagger(classifier_file, settings.STANFORD_NER_JAR)

    def predict_sentence(self, sentence):
        tokenized_sentence = tokenizer.tokenize_word(sentence)
        tags = self.classifier.tag(tokenized_sentence)
        mapped_tags = [(i[0], map_tag(i[1])) for i in tags]
        print mapped_tags  # TODO: remove
        return mapped_tags


def map_tag(tag):
    if tag == 'O':
        return 'O'
    elif tag == 'MISC':
        return 'MISC'
    elif tag == 'LOCATION':
        return 'LOC'
    elif tag == 'PERSON':
        return 'PER'
    elif tag == 'ORGANIZATION':
        return 'ORG'
    else:
        print("Don't know how to map tag {}".format(tag))
        return 'O'
        # raise ValueError("Don't know how to map tag {}".format(tag))
