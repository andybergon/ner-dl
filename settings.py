import os


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DATA_ROOT = os.path.join(PROJECT_ROOT, 'data')

MODEL_ROOT = os.path.join(DATA_ROOT, 'model')
TRAINING_ROOT = os.path.join(DATA_ROOT, 'training')
WORD2VEC_ROOT = os.path.join(DATA_ROOT, 'word2vec')

MIDNAMES_FILE = os.path.join(DATA_ROOT, 'mid', 'mid_name_types.tsv')
WORD2VEC_TXT_FILE = os.path.join(WORD2VEC_ROOT, 'w2v.txt')
