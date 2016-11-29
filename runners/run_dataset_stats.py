from nerdl.dataset.dataset_stats_calculator import DatasetStatsCalculator
from settings import path_settings

# dataset_fp = path_settings.FIGER_DATASET_CW_TAGS_FILE
dataset_fp = path_settings.CW_TRAIN_FILE
# dataset_fp = path_settings.CW_TEST_FILE

DatasetStatsCalculator(dataset_fp).calculate_sentence_length(sentence_nb=0, print_every=0)
