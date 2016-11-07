from tagger import Tagger


class StanfordFourTagger(Tagger):
    def __init__(self):
        pass

    def tag(self, entity_types):
        stanford_types = convert_freebase_to_stanford_types(entity_types)
        stanford_types = ','.join(stanford_types)
        return stanford_types


def convert_freebase_to_stanford_types(freebase_types):
    stanford_types = []
    entity_domain = get_types_domain(freebase_types)

    if 'location' in entity_domain:  # LOC have preference over ORG
        stanford_types.append('LOC')
    elif 'organization' in entity_domain:
        stanford_types.append('ORG')
    elif 'people' in entity_domain:
        stanford_types.append('PER')
    else:
        stanford_types.append('MISC')

    return stanford_types


def get_types_domain(entity_types):
    entity_domains = set()

    for entity_type in entity_types:
        entity_domain = entity_type.split('.')[0]
        entity_domains.add(entity_domain)

    return entity_domains
