from settings import path_settings
from tagger import Tagger


class CWTop275Tagger(Tagger):
    def __init__(self):
        self.top_types_fp = path_settings.CW_TOP250_TYPES_FILE
        self.top_types = []  # e.g. [american_football.football_coach, ..., visual_art.visual_artist]

        self.initialize_top_list()

    def initialize_top_list(self):
        with open(self.top_types_fp, 'r') as list_f:
            for line in list_f:
                top_type = line.rstrip('\n')
                self.top_types.append(top_type)

    def tag(self, entity_types):
        top_cw_types = self.cut_to_top275_cw_types(entity_types)
        return top_cw_types

    def cut_to_top275_cw_types(self, freebase_types):
        """

        :param freebase_types: e.g. [a, b, c]
        :return: e.g. [a, c]
        """
        top_cw_types = []

        for freebase_type in freebase_types:
            if freebase_type in self.top_types:
                top_cw_types.append(freebase_type)

        if len(top_cw_types) == 0:
            top_cw_types.append('O')

        top_cw_types = sorted(set(top_cw_types))

        return top_cw_types
