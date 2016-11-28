import time

from nerdl.dataset.dataset_iterator import DatasetIterator
from nerdl.evaluation.model_evaluation_entities import EvaluatorEntities
from nerdl.ner.sentence2entities import Sentence2Entities
from settings import path_settings
from settings import settings

start = time.time()  # can use time.clock()

################################################################################
# settings.EVALUATION_CLASS_LIST
settings.EVALUATION_CLASS_LIST = settings.FIGER_RAW_CLASS_LIST

dataset_correct_fp = path_settings.FIGER_GOLD_FILE
dataset_predict_fp = path_settings.FIGER_GOLD_OUTPUT_FILE

ee = EvaluatorEntities(dataset_correct_fp, dataset_predict_fp)
ee.evaluate_model(test_sentences_nb=0, print_every=100)
################################################################################

end = time.time()
print('{} seconds'.format(str(end - start)))
