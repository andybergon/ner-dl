import time

from nerdl.evaluation.model_evaluation_keras import EvaluatorKerasMultiLabel
from nerdl.evaluation.model_evaluation_multi_label import EvaluatorMultiLabel
from nerdl.ner.models.figer.figer_model import FigerNERModel
from nerdl.ner.models.keras.keras_model import KerasNERModel
from settings import path_settings

# path_settings.WORD2VEC_TXT_FILE
# path_settings.TEST_FILE

# path_settings.WORD2VEC_TXT_FILE = path_settings.CW_W2V_TXT_FILE.replace('.txt', '-old.txt')
# path_settings.TEST_FILE = path_settings.TEST_FILE.replace('test.tsv', 'test_1000k.tsv')
path_settings.WORD2VEC_TXT_FILE = path_settings.FIGER_W2V_TXT_FILE
path_settings.TEST_FILE = path_settings.FIGER_TEST_FILE

start = time.time()  # can use time.clock()

print('>> Loading model...')
start_import_model = time.time()
model = KerasNERModel()
model.load()  # loads 'model-to-load.h5'
end_import_model = time.time()
print('<< Loaded model in {} seconds.\n'.format(str(end_import_model - start_import_model)))

# model = FigerNERModel()

# evaluator = EvaluatorMultiLabel(model)
# evaluator.evaluate_model(test_sentences_nb=1000, print_every=100)

k_evaluator = EvaluatorKerasMultiLabel(model)
threshold_dict = k_evaluator.evaluate_keras_model_increasing_threshold(samples_to_test=500, print_every=0)

# comparator = Comparator(class_list)  # TODO: fix, read class list from parameter
# comparator.compare_models(print_every=20)

end = time.time()

print('{} seconds'.format(str(end - start)))
