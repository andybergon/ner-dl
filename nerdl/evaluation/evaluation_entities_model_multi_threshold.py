from nerdl.evaluation.evaluation_entities_model import EvaluatorEntitiesModel


class EvaluatorMultiThreshold(EvaluatorEntitiesModel):
    def __init__(self, di, s2e, model):
        EvaluatorEntitiesModel.__init__(self, di, s2e, model)

    def evaluate_increasing_threshold(self, test_sentences_nb=1000, print_every=0, thresholds=[0.01]):
        thresholds_stats = {}

        for threshold in thresholds:
            print('THRESHOLD = {}'.format(threshold))
            p, r, f1 = self.evaluate(test_sentences_nb=test_sentences_nb,
                                     print_every=print_every,
                                     model_threshold=threshold)
            self.initialize_stats()  # resets stats
            thresholds_stats[threshold] = p, r, f1

        print('Easy Excel Import:')
        for k, v in sorted(thresholds_stats.items()):
            print('{}\t{}\t{}\t{}'.format(k, v[0], v[1], v[2]))

        return thresholds_stats
