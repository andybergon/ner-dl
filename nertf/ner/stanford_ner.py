from nltk.tag.stanford import StanfordNERTagger

import settings


class StanfordNERModel():
    def __init__(self):
        self.classifier = StanfordNERTagger(settings.STANFORD_NER_CLASSIFIER, settings.STANFORD_NER_JAR)

    def tag(self, sentence):
        self.classifier.tag(sentence.split())  # TODO: use tokenizer
