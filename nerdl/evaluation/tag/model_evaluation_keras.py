from nerdl.evaluation.tag.model_evaluation_tags_multi_label import EvaluatorMultiLabel
from settings import settings


class EvaluatorKerasMultiLabel(EvaluatorMultiLabel):
    def __init__(self, model):
        EvaluatorMultiLabel.__init__(self, model)

    def evaluate_keras_model_increasing_cutoff(self, samples_to_test=1000, print_every=0):
        settings.KERAS_DECODER = 'top'
        cutoffs = settings.KERAS_TEST_CUTOFFS
        cutoffs_stats = {}

        for cutoff in cutoffs:
            settings.KERAS_TOP_DECODER_NB = cutoff
            print('CUTOFF = {}'.format(cutoff))
            p, r, f1 = self.evaluate_model(test_sentences_nb=samples_to_test, print_every=print_every)
            self.initialize_stats()  # resets stats
            cutoffs_stats[cutoff] = p, r, f1

        print('Easy Excel Import:')
        for k, v in sorted(cutoffs_stats.items()):
            print('{}\t{}\t{}\t{}'.format(k, v[0], v[1], v[2]))

        return cutoffs_stats

    def evaluate_keras_model_increasing_threshold(self, samples_to_test=1000, print_every=0):
        settings.KERAS_DECODER = 'threshold'
        thresholds = settings.KERAS_TEST_THRESHOLDS
        thresholds_stats = {}

        for threshold in thresholds:
            settings.KERAS_THRESHOLD_NB = threshold
            print('THRESHOLD = {}'.format(threshold))
            p, r, f1 = self.evaluate_model(test_sentences_nb=samples_to_test, print_every=print_every)
            self.initialize_stats()  # resets stats
            thresholds_stats[threshold] = p, r, f1

        print('Easy Excel Import:')
        for k, v in sorted(thresholds_stats.items()):
            print('{}\t{}\t{}\t{}'.format(k, v[0], v[1], v[2]))

        return thresholds_stats
