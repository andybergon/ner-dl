from settings import path_settings
from tagger import Tagger


class FigerTagger(Tagger):
    def __init__(self):
        self.mapping_file = path_settings.FIGER_ENTITY_MAPPING
        self.freebase2figer_map = {}  # e.g. AMUSEMENT_PARKS.PARK -> PARK

        self.initialize_map()

    def initialize_map(self):
        with open(self.mapping_file, 'rt') as mapping_f:
            for line in mapping_f:
                freebase_type, figer_type = line.rstrip('\n').split('\t')
                freebase_type = freebase_type.replace('/', '', 1).replace('/', '.')
                figer_type = figer_type.replace('/', '', 1).replace('/', '.')
                self.freebase2figer_map[freebase_type] = figer_type

    def tag(self, entity_types):
        figer_types = self.convert_freebase_to_figer_types(entity_types)
        return figer_types

    def convert_freebase_to_figer_types(self, freebase_types):
        """

        :param freebase_types: e.g. [AWARD.AWARD, MUSIC.ALBUM]
        :return: e.g. [AWARD, MUSIC]
        """
        figer_types = []

        for freebase_type in freebase_types:
            if freebase_type in self.freebase2figer_map:
                figer_type = self.freebase2figer_map[freebase_type]
                figer_types.append(figer_type)

        figer_types = sorted(set(figer_types))

        if len(figer_types) == 0:
            figer_types.append('MISC')

        return figer_types
