import time

from nerdl.dataset.taggers.cw_top275_tagger import CWTop275Tagger
from nerdl.dataset.taggers.figer_tagger import FigerTagger
from nerdl.dataset.taggers.stanford_four_tagger import StanfordFourTagger
from nerdl.evaluation.evaluation_entities_files import EvaluatorEntitiesFiles
from nerdl.evaluation.evaluation_entities_model import EvaluatorEntitiesModel
from nerdl.evaluation.evaluation_entities_model_multi_threshold import EvaluatorMultiThreshold
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
# settings.MAX_SENTENCE_LEN
# settings.TAG2VEC_CLASS_LIST
# settings.EVALUATION_CLASS_LIST
# path_settings.WORD2VEC_TXT_FILE
# path_settings.TEST_FILE

settings.MAX_SENTENCE_LEN = 50

settings.EVALUATION_CLASS_LIST = settings.TAG2VEC_CLASS_LIST = settings.CW_TOP275_CLASS_LIST
# settings.EVALUATION_CLASS_LIST = settings.TAG2VEC_CLASS_LIST = settings.FIGER_CLASS_LIST
# settings.EVALUATION_CLASS_LIST = settings.TAG2VEC_CLASS_LIST = settings.STANFORD_FOUR_CLASS_LIST

path_settings.WORD2VEC_TXT_FILE = path_settings.CW_W2V_TXT_FILE
dataset_correct_fp = path_settings.TEST_FILE = path_settings.CW_TEST_FILE

# path_settings.WORD2VEC_TXT_FILE = path_settings.FIGER_W2V_TXT_FILE
# dataset_correct_fp = path_settings.TEST_FILE = path_settings.FIGER_GOLD_NOT_BIO_FILE

print('>> Loading model...')
start_import_model = time.time()
model = KerasNERModel()
model.load()  # loads 'model-to-load.h5'
end_import_model = time.time()
print('<< Loaded model in {} seconds.\n'.format(str(end_import_model - start_import_model)))

##############################
di = DatasetIterator(dataset_correct_fp)

tagger = CWTop275Tagger()
# tagger = FigerTagger()
# tagger = StanfordFourTagger()

s2e = Sentence2Entities(is_bio=True, tagger=tagger)

emt = EvaluatorMultiThreshold(di, s2e, model)

thresholds = [0.001, 0.0025, 0.005, 0.0075, 0.01, 0.025, 0.05, 0.1]  # cw-275
# thresholds = [0.025, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3]  # figer
# thresholds = [0.025, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3]  # stanford

emt.evaluate_increasing_threshold(test_sentences_nb=1000, print_every=0, thresholds=thresholds)
################################################################################
# # settings.EVALUATION_CLASS_LIST
#
# settings.EVALUATION_CLASS_LIST = settings.CW_TOP275_CLASS_LIST  # needed? used in Evaluator
#
# # dataset_correct_fp = path_settings.FIGER_GOLD_BIO_FILE
# dataset_correct_fp = path_settings.CW_TEST_FILE
# di = DatasetIterator(dataset_correct_fp)
# correct_s2e = Sentence2Entities(is_bio=True)
#
# # test_fp = path_settings.FIGER_GOLD_BIO_FILE
# test_fp = path_settings.CW_TEST_FILE
# mi = ModelIterator(test_fp, model)
# predict_s2e = Sentence2Entities(is_bio=True)
#
# ee = EvaluatorEntitiesFiles(di, mi, correct_s2e, predict_s2e)
# ee.evaluate(test_sentences_nb=100, print_every=100)
################################################################################
# settings.EVALUATION_CLASS_LIST = settings.CW_TOP275_CLASS_LIST  # needed? used in Evaluator
#
# dataset_correct_fp = path_settings.CW_TEST_FILE
# di = DatasetIterator(dataset_correct_fp)
# tagger = CWTop275Tagger()
# s2e = Sentence2Entities(is_bio=True, tagger=tagger)
#
# ee = EvaluatorEntitiesModel(di, s2e, model)
# ee.evaluate(test_sentences_nb=100, print_every=100, model_threshold=0.1)
################################################################################

end = time.time()
print('{} seconds'.format(str(end - start)))
