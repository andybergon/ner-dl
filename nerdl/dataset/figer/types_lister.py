from settings import path_settings


def list_raw_figer_types():
    figer_types = {}
    with open(path_settings.FIGER_ENTITY_MAPPING, 'r') as mapping_f:
        for line in mapping_f:
            freebase_type, figer_type = line.rstrip('\n').split('\t')

            if figer_type in figer_types:
                figer_types[figer_type] += 1
            else:
                figer_types[figer_type] = 1

    # print(sorted(figer_types.items(), key=operator.itemgetter(1), reverse=True))

    figer_types = figer_types.keys()
    figer_types.sort()

    return figer_types


def list_figer_types():
    figer_types = {}
    with open(path_settings.FIGER_ENTITY_MAPPING, 'r') as mapping_f:
        for line in mapping_f:
            freebase_type, figer_type = line.rstrip('\n').split('\t')
            figer_type = figer_type.replace('/', '', 1).replace('/', '.')

            if figer_type in figer_types:
                figer_types[figer_type] += 1
            else:
                figer_types[figer_type] = 1

    figer_types = figer_types.keys()

    return figer_types


def list_top275_cw_types():
    cw_top_types = []
    with open(path_settings.CW_TOP250_TYPES_FILE, 'r') as list_f:
        for line in list_f:
            cw_top_type = line.rstrip('\n')
            cw_top_types.append(cw_top_type)

    return cw_top_types
