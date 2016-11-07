from nltk.tag.stanford import StanfordNERTagger

import nerdl.ner.utils.tokenizer
import path_settings


class StanfordNERModel:
    def __init__(self, nb_classes=4):
        if nb_classes == 4:
            classifier_file = path_settings.STANFORD_NER_CLASSIFIER_4C
        elif nb_classes == 3:
            classifier_file = path_settings.STANFORD_NER_CLASSIFIER_3C
        else:
            raise ValueError('Number of classes not supported')

        self.classifier = StanfordNERTagger(classifier_file, path_settings.STANFORD_NER_JAR)

    def predict_tokenized_sentence(self, tokenized_sentence):
        tags = self.classifier.tag(tokenized_sentence)
        mapped_tags = [(i[0], map_tag(i[1])) for i in tags]

        return mapped_tags

    def predict_sentence(self, sentence):
        tokenized_sentence = nerdl.ner.utils.tokenizer.tokenize_word(sentence)

        return self.predict_tokenized_sentence(tokenized_sentence)


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
