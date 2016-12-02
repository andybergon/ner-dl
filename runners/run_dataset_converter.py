import time

from nerdl.dataset import dataset_splitter_shortener
from nerdl.dataset.cw.cw_dataset_generator import CWDatasetGenerator
from nerdl.dataset.dataset_converter import DatasetConverter
from nerdl.dataset.dataset_splitter_shortener import DatasetSplitterShortener
from nerdl.dataset.figer import figer_gold_converter
from nerdl.dataset.taggers.cw_uppoint_cw_lowpoint_tagger import CwUpPointCwLowPointTagger
from settings import path_settings

start = time.time()  # can use time.clock()

################################################################################
# dataset_fp = path_settings.CW_DATASET_CW_TAGS_FILE
# dataset_converted_fp = path_settings.CW_DATASET_CW_TAGS_FILE.replace('cw-tags', 'cw-tags-new')
# tagger = CwUpPointCwLowPointTagger()
#
# print('>> Converting Dataset...')
# ds_converter = DatasetConverter(dataset_fp, dataset_converted_fp, tagger)
# ds_converter.convert(sentence_nb=3000000, print_every=300000)
################################################################################
# dataset_fp = path_settings.FIGER_DATASET_FG_TAGS_FILE
# train_fp = path_settings.FIGER_TRAIN_FILE
# test_fp = path_settings.FIGER_TEST_FILE
#
# dss = DatasetSplitterShortener(dataset_fp, train_fp, test_fp)
# dss.split_and_shorten()
################################################################################

end = time.time()
print('{} seconds'.format(str(end - start)))
