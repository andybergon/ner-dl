import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

DATA_ROOT = os.path.join(PROJECT_ROOT, 'data')

MID_ROOT = os.path.join(DATA_ROOT, 'mid')
MIDNAMES_FILE = os.path.join(MID_ROOT, 'mid_name_types.tsv')

CW_CORPUS_FILE = os.path.join(DATA_ROOT, 'cw', 'cw_1_corpus.tsv')
CW_CORPUS_FILE_EXAMPLE = os.path.join(DATA_ROOT, 'cw', 'cw_1_corpus_example.tsv')

MODEL_ROOT = os.path.join(DATA_ROOT, 'model')
MODEL_FILE = os.path.join(MODEL_ROOT, 'model.h5')
MODEL_TO_LOAD_FILE = os.path.join(MODEL_ROOT, 'model-to-load.h5')
MODEL_CHECKPOINT_FILE = os.path.join(MODEL_ROOT, 'model-checkpoint.hdf5')  # using MODEL_FILE itself

DATASET_ROOT = os.path.join(DATA_ROOT, 'dataset')
CW_DATASET_CW_TAGS_FILE = os.path.join(DATASET_ROOT, 'cw-dataset', 'cw-dataset-cw-tags.tsv')
CW_DATASET_FG_TAGS_FILE = os.path.join(DATASET_ROOT, 'cw-dataset', 'cw-dataset-figer-tags.tsv')
FIGER_DATASET_CW_TAGS_FILE = os.path.join(DATASET_ROOT, 'figer-dataset', 'figer-dataset-cw-tags.tsv')
FIGER_DATASET_FG_TAGS_FILE = os.path.join(DATASET_ROOT, 'figer-dataset', 'figer-dataset-figer-tags.tsv')

TRAINING_ROOT = os.path.join(DATA_ROOT, 'training')
TRAINING_FILE = os.path.join(TRAINING_ROOT, 'training.tsv')
TRAINING_CHECKPOINT_FILE = os.path.join(TRAINING_ROOT, 'training-checkpoint.txt')

TEST_ROOT = os.path.join(DATA_ROOT, 'test')
TEST_FILE = os.path.join(TEST_ROOT, 'test.tsv')
TEST_CHECKPOINT_FILE = os.path.join(TEST_ROOT, 'test-checkpoint.txt')

WORD2VEC_ROOT = os.path.join(DATA_ROOT, 'word2vec')
WORD2VEC_FILE = os.path.join(WORD2VEC_ROOT, 'w2v')  # not needed
WORD2VEC_TXT_FILE = os.path.join(WORD2VEC_ROOT, 'w2v.txt')
CW_W2V_TXT_FILE = os.path.join(WORD2VEC_ROOT, 'cw', 'w2v.txt')

FIGER_ROOT = os.path.join(DATA_ROOT, 'figer')
FIGER_TRAIN_FILE = os.path.join(TRAINING_ROOT, 'figer', 'figer-train.tsv')
FIGER_TEST_FILE = os.path.join(TEST_ROOT, 'figer', 'figer-test.tsv')
FIGER_ENTITY_MAPPING = os.path.join(FIGER_ROOT, 'entity-types-mapping')
FIGER_W2V_TXT_FILE = os.path.join(WORD2VEC_ROOT, 'figer', 'w2v.txt')
FIGER_GOLD_FILE = os.path.join(FIGER_ROOT, 'exp.label')

FIGER_GOLD_BIO_FILE = os.path.join(TEST_ROOT, 'figer-gold', 'figer-gold-bio.tsv')
FIGER_GOLD_NOT_BIO_FILE = os.path.join(TEST_ROOT, 'figer-gold', 'figer-gold-not-bio.tsv')

FIGER_SENTENCES_FILE = os.path.join(DATA_ROOT, 'sentences', 'figer', 'figer-sentences.txt')
CW_SENTENCES_FILE = os.path.join(DATA_ROOT, 'sentences', 'cw', 'cw-sentences.txt')
SENTENCES_FILE = CW_SENTENCES_FILE

STANFORD_NER_FOLDER = os.path.join(PROJECT_ROOT, 'stanford-ner-2014-08-27')
# [LOCATION, PERSON, ORGANIZATION]
STANFORD_NER_CLASSIFIER_3C = os.path.join(STANFORD_NER_FOLDER, 'classifiers', 'english.all.3class.distsim.crf.ser.gz')
# [LOCATION, PERSON, ORGANIZATION, MISC]
STANFORD_NER_CLASSIFIER_4C = os.path.join(STANFORD_NER_FOLDER, 'classifiers', 'english.conll.4class.distsim.crf.ser.gz')
STANFORD_NER_JAR = os.path.join(STANFORD_NER_FOLDER, 'stanford-ner.jar')  # can be set in CLASSPATH=

EVALUATOR_LOG_FILE = os.path.join(DATA_ROOT, 'evaluation', 'evaluation.txt')  # DEPRECATED???
