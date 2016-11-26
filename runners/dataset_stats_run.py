from nerdl.dataset.dataset_stats_calculator import DatasetStatsCalculator
from settings import path_settings

dataset_fp = path_settings.FIGER_DATASET_CW_TAGS_FILE

DatasetStatsCalculator(dataset_fp).calculate_sentence_length()
