from nerdl.dataset.figer import types_lister

MAX_SENTENCE_LEN = 80

STANFORD_FOUR_CLASS_LIST = ['LOC', 'PER', 'ORG', 'MISC', 'O', 'NIL']
figer_only_types = types_lister.list_figer_types()
FIGER_CLASS_LIST = figer_only_types + ['NIL', 'MISC', 'O']
