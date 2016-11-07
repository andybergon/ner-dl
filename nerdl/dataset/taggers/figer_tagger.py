import path_settings
from tagger import Tagger


class FigerTagger(Tagger):
    def __init__(self):
        self.mapping_file = path_settings.FIGER_ENTITY_MAPPING

    def tag(self, entity_types):
        figer_types = self.convert_freebase_to_figer_types(entity_types)
        figer_types = ','.join(figer_types)
        return figer_types

    def convert_freebase_to_figer_types(self, freebase_types):
        figer_types = []

        # TODO: optimize, open file at construction and method to close
        with open(self.mapping_file, 'rt') as mapping_f:
            for fb_type in freebase_types:
                mapping_f.seek(0)
                for line in mapping_f:
                    freebase_type, figer_type = line.rstrip('\n').split('\t')
                    freebase_type = freebase_type.replace('/', '', 1).replace('/', '.')

                    if fb_type == freebase_type:
                        figer_type = figer_type.replace('/', '', 1).replace('/', '.')
                        figer_types.append(figer_type.upper())
                        break

        figer_types = sorted(set(figer_types))

        if len(figer_types) == 0:
            figer_types.append('MISC')

        return figer_types
