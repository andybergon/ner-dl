import os

from settings import path_settings


class MidnamesManager:
    def __init__(self):
        self.midnames_fp = path_settings.MIDNAMES_FILE
        self.midnames_f = self.open_midnames_file()

    def open_midnames_file(self):
        return open(self.midnames_fp, 'r')

    def close_midnames_file(self):
        self.midnames_f.close()

    def get_row_by_id(self, searched_row_id):
        step = os.path.getsize(self.midnames_fp) / 2.
        step_dimension = step
        last_row_id = ""

        while True:
            self.midnames_f.seek(int(step), 0)  # absolute position
            # self.midnames_f.seek(int(step), 1)  # relative position
            seek_to(self.midnames_f, '\n')
            row = parse_row(self.midnames_f.readline())
            row_id = row[0]

            if row_id == last_row_id:
                raise ValueError(searched_row_id)
            else:
                last_row_id = row_id

            if row_id == searched_row_id:
                return row[1]  # ritorno l'intera riga
            elif searched_row_id < row_id:
                # step /= 2.
                # step = step * -1 if step < 0 else step
                step_dimension /= 2.
                step = step - step_dimension
            else:  # searched_row_id > row_id
                # step /= 2.
                # step = step * -1 if step > 0 else step
                step_dimension /= 2.
                step = step + step_dimension

    def get_rows_in_range(self, start_range, end_range):
        # rows_list = []

        for line in self.midnames_f:
            current_id = line.split('\t')[0]
            if start_range <= current_id <= end_range:
                print line
                #             entity_id, entity_name, entity_type = line.replace('\n', '').split('\t')
                #             rows_list.append((entity_id, entity_name, entity_type))
                # return rows_list

    def count_unique_types(self):
        entity_num = 0
        unique_types = {}

        for line in self.midnames_f:
            entity_num += 1
            _, _, types = line.rstrip('\n').split('\t')
            types = types.split(',')

            for e_type in types:
                if e_type in unique_types:
                    unique_types[e_type] += 1
                else:
                    unique_types[e_type] = 1

            if entity_num % 1000000 == 0:
                print('{}M entities -> {} unique types'.format(entity_num / 1000000, len(unique_types)))

        print(sorted(unique_types.items(), key=lambda x: x[1], reverse=True))

        return unique_types


# seek to first character c before the current position
def seek_to(f, c):
    while f.read(1) != c:
        f.seek(-2, 1)


def parse_row(row):
    return row.split('\t')[0], row
