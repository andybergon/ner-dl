import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

DATA_ROOT = os.path.join(PROJECT_ROOT, 'data')

MODEL_ROOT = os.path.join(DATA_ROOT, 'model')
CORPUS_FILE = os.path.join(DATA_ROOT, 'sentences', 'cw_1_sentences.tsv')
CORPUS_FILE_EXAMPLE = os.path.join(DATA_ROOT, 'sentences', 'cw_1_sentences_example.tsv')
REPLACED_CORPUS_FILE = os.path.join(DATA_ROOT, 'replaced', 'cw_1_replaced.tsv')

MODEL_FILE = os.path.join(MODEL_ROOT, 'model.h5')
MODEL_TO_LOAD_FILE = os.path.join(MODEL_ROOT, 'model-to-load.h5')
MODEL_CHECKPOINT_FILE = os.path.join(MODEL_ROOT, 'model-checkpoint.hdf5')  # using MODEL_FILE for now

TRAINING_ROOT = os.path.join(DATA_ROOT, 'training')
TRAINING_FILE = os.path.join(TRAINING_ROOT, 'training.tsv')
TRAINING_CHECKPOINT_FILE = os.path.join(TRAINING_ROOT, 'training-checkpoint.txt')

TEST_ROOT = os.path.join(DATA_ROOT, 'test')
TEST_FILE = os.path.join(TEST_ROOT, 'test.tsv')
TEST_CHECKPOINT_FILE = os.path.join(TEST_ROOT, 'test-checkpoint.txt')

WORD2VEC_ROOT = os.path.join(DATA_ROOT, 'word2vec')
WORD2VEC_FILE = os.path.join(WORD2VEC_ROOT, 'w2v')  # not needed
WORD2VEC_TXT_FILE = os.path.join(WORD2VEC_ROOT, 'w2v.txt')

MID_ROOT = os.path.join(DATA_ROOT, 'mid')
MIDNAMES_FILE = os.path.join(MID_ROOT, 'mid_name_types.tsv')
FIGER_ENTITY_MAPPING = os.path.join(MID_ROOT, 'entity-types-mapping')

STANFORD_NER_FOLDER = os.path.join(PROJECT_ROOT, 'stanford-ner-2014-08-27')
# [LOCATION, PERSON, ORGANIZATION]
STANFORD_NER_CLASSIFIER_3C = os.path.join(STANFORD_NER_FOLDER, 'classifiers', 'english.all.3class.distsim.crf.ser.gz')
# [LOCATION, PERSON, ORGANIZATION, MISC]
STANFORD_NER_CLASSIFIER_4C = os.path.join(STANFORD_NER_FOLDER, 'classifiers', 'english.conll.4class.distsim.crf.ser.gz')
STANFORD_NER_JAR = os.path.join(STANFORD_NER_FOLDER, 'stanford-ner.jar')  # can be set in CLASSPATH=

EVALUATOR_LOG_FILE = os.path.join(DATA_ROOT, 'evaluation', 'evaluation.txt')
