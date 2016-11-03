import path_settings


def list_figer_types():
    figer_types = {}
    with open(path_settings.FIGER_ENTITY_MAPPING, 'r') as mapping_f:
        for line in mapping_f:
            freebase_type, figer_type = line.rstrip('\n').split('\t')
            figer_type = figer_type.replace('/', '', 1).replace('/', '.').upper()

            if figer_type in figer_types:
                figer_types[figer_type] += 1
            else:
                figer_types[figer_type] = 1

    figer_types = figer_types.keys()

    return figer_types
