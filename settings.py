import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DATA_ROOT = os.path.join(PROJECT_ROOT, 'data')

MODEL_ROOT = os.path.join(DATA_ROOT, 'model')
TRAINING_ROOT = os.path.join(DATA_ROOT, 'training')
WORD2VEC_ROOT = os.path.join(DATA_ROOT, 'word2vec')

MIDNAMES_FILE = os.path.join(DATA_ROOT, 'mid', 'mid_name_types.tsv')
WORD2VEC_TXT_FILE = os.path.join(WORD2VEC_ROOT, 'w2v.txt')

STANFORD_NER_FOLDER = os.path.join(PROJECT_ROOT, 'stanford-ner-2014-08-27')
STANFORD_NER_CLASSIFIER = os.path.join(STANFORD_NER_FOLDER, 'classifiers', 'english.all.3class.distsim.crf.ser.gz')
STANFORD_NER_JAR = os.path.join(STANFORD_NER_FOLDER, 'stanford-ner.jar')  # can be set in CLASSPATH=
