import time

from nerdl.evaluation.evaluation_entities_files import EvaluatorEntitiesFiles
from nerdl.ner.iterators.dataset_iterator import DatasetIterator
from nerdl.ner.iterators.model_iterator import ModelIterator
from nerdl.ner.models.keras.keras_model import KerasNERModel
from nerdl.ner.sentence2entities import Sentence2Entities
from settings import path_settings
from settings import settings

start = time.time()  # can use time.clock()

################################################################################
# settings.EVALUATION_CLASS_LIST
# settings.EVALUATION_CLASS_LIST = settings.FIGER_RAW_CLASS_LIST
#
# dataset_correct_fp = path_settings.FIGER_GOLD_FILE
# dataset_predict_fp = path_settings.FIGER_GOLD_OUTPUT_FILE
#
# di_correct = DatasetIterator(dataset_correct_fp)
# di_predict = DatasetIterator(dataset_predict_fp)
#
# correct_s2e = Sentence2Entities(is_bio=True)
# predict_s2e = Sentence2Entities(is_bio=True)
#
# ee = EvaluatorEntities(di_correct, di_predict, correct_s2e, predict_s2e)
# ee.evaluate(test_sentences_nb=0, print_every=100)
################################################################################
# path_settings.WORD2VEC_TXT_FILE
# path_settings.TEST_FILE
# settings.MAX_SENTENCE_LEN

settings.MAX_SENTENCE_LEN = 50
settings.TAG2VEC_CLASS_LIST = settings.CW_TOP275_CLASS_LIST

# path_settings.WORD2VEC_TXT_FILE = path_settings.FIGER_W2V_TXT_FILE
# path_settings.TEST_FILE = path_settings.FIGER_GOLD_NOT_BIO_FILE

# path_settings.WORD2VEC_TXT_FILE = path_settings.CW_W2V_TXT_FILE
path_settings.WORD2VEC_TXT_FILE = path_settings.CW_W2V_TXT_FILE.replace('.txt', '-old.txt')
# path_settings.TEST_FILE = path_settings.FIGER_GOLD_NOT_BIO_FILE

print('>> Loading model...')
start_import_model = time.time()
model = KerasNERModel()
model.load()  # loads 'model-to-load.h5'
end_import_model = time.time()
print('<< Loaded model in {} seconds.\n'.format(str(end_import_model - start_import_model)))
########################################
# sentence = 'Trump is the president of the United States'
# entities = ['Trump', 'United States']

word_bio = [('Trump', 'B'), ('is', 'O'), ('the', 'O'), ('president', 'O'), ('of', 'O'), ('the', 'O'),
            ('United', 'B'), ('States', 'I')]
model.predict_given_bio(word_bio, 0.01)

########################################
# # settings.EVALUATION_CLASS_LIST
#
# settings.EVALUATION_CLASS_LIST = settings.FIGER_OLD_CLASS_LIST
#
# dataset_correct_fp = path_settings.FIGER_GOLD_BIO_FILE
# di = DatasetIterator(dataset_correct_fp)
# correct_s2e = Sentence2Entities(is_bio=True)
#
# test_fp = path_settings.FIGER_GOLD_BIO_FILE
# mi = ModelIterator(test_fp, model)
# predict_s2e = Sentence2Entities(is_bio=False)
#
# ee = EvaluatorEntities(di, mi, correct_s2e, predict_s2e)
# ee.evaluate(test_sentences_nb=0, print_every=100)
################################################################################

end = time.time()
print('{} seconds'.format(str(end - start)))
