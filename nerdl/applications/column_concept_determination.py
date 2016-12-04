from settings import path_settings


class CCD:
    def __init__(self):
        self.persons = {}
        self.others = {}

        self.persons_stats = {}
        self.others_stats = {}

        self.load_person_lector()
        self.load_other_lector()

    def load_person_lector(self):
        with open(path_settings.PERSON_LECTOR_FILE) as f:
            for line in f:
                mid, name, types = line.rstrip().split('\t')
                types = types.split(',')
                self.persons[mid] = name, types

    def load_other_lector(self):
        with open(path_settings.OTHERS_LECTOR_FILE) as f:
            for line in f:
                mid, name, types = line.rstrip().split('\t')
                types = types.split(',')
                self.others[mid] = name, types

    def calculate_stats(self):
        e1_absent_sentence_nb = 0
        e2_absent_sentence_nb = 0
        e1_absent_list = []
        e2_absent_list = []

        with open(path_settings.SENTENCES_LECTOR_FILE) as f:
            for line in f:
                e1, relation, e2, count = line.rstrip().split('\t')

                if e1 in self.persons:
                    name_e1, types_e1 = self.persons[e1]
                    # print('{} in person as {}'.format(e1, name_e1))

                    if e1 not in self.persons_stats:
                        self.persons_stats[e1] = {}

                    for type_e1 in types_e1:
                        if type_e1 in self.persons_stats[e1]:
                            self.persons_stats[e1][type_e1] += 1
                        else:
                            self.persons_stats[e1][type_e1] = 1

                elif e1 in self.others:
                    name_e1, types_e1 = self.others[e1]
                    # print('{} in others'.format(e1, name_e1))

                    if e1 not in self.others_stats:
                        self.others_stats[e1] = {}

                    for type_e1 in types_e1:
                        if type_e1 in self.others_stats[e1]:
                            self.others_stats[e1][type_e1] += 1
                        else:
                            self.others_stats[e1][type_e1] = 1

                else:
                    e1_absent_sentence_nb += 1
                    if e1 not in e1_absent_list:
                        e1_absent_list.append(e1)
                    # print('e1 mid {} NOT present!'.format(e1))
                    # raise ValueError('mid {} NOT present!'.format(e1))

                if e2 in self.persons:
                    name_e2, types_e2 = self.persons[e2]
                    # print('{} in person as {}'.format(e2, name_e2))

                    if e2 not in self.persons_stats:
                        self.persons_stats[e2] = {}

                    for type_e2 in types_e2:
                        if type_e2 in self.persons_stats[e2]:
                            self.persons_stats[e2][type_e2] += 1
                        else:
                            self.persons_stats[e2][type_e2] = 1

                elif e2 in self.others:
                    name_e2, types_e2 = self.others[e2]
                    # print('{} in others'.format(e2, name_e2))

                    if e2 not in self.others_stats:
                        self.others_stats[e2] = {}

                    for type_e2 in types_e2:
                        if type_e2 in self.others_stats[e2]:
                            self.others_stats[e2][type_e2] += 1
                        else:
                            self.others_stats[e2][type_e2] = 1

                else:
                    e2_absent_sentence_nb += 1
                    if e2 not in e2_absent_list:
                        e2_absent_list.append(e2)
                    # print('e2 mid {} NOT present!'.format(e2))

            print('sentences absent - e1: {} - e2: {}'.format(e1_absent_sentence_nb, e2_absent_sentence_nb))
            print('mid absent - e1: {} - e2: {}'.format(len(e1_absent_list), len(e2_absent_list)))

            self.print_stats()

    def print_stats(self):
        print('PERSONS TYPES:')
        print_generic_stats(self.persons_stats)

        print('OTHERS TYPES:')
        print_generic_stats(self.others_stats)


def print_generic_stats(stats_dict):
    for entity in stats_dict:
        entity_types = []
        for type in stats_dict[entity]:
            # TODO: tornali ordinati per valore!
            entity_types.append(type)
        print('{} - {}'.format(entity, entity_types))


if __name__ == '__main__':
    ccd = CCD()
    ccd.calculate_stats()
