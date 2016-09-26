import os

mid_name_file = os.path.join(os.path.dirname(__file__), 'data/mid_name_types.tsv')


# seek to first character c before the current position
def seek_to(f, c):
    while f.read(1) != c:
        f.seek(-2, 1)


def parse_row(row):
    return row.split('\t')[0], row


# TODO: check if always working for all ids
def get_row_by_id(searched_row_id):
    step = os.path.getsize(mid_name_file) / 2.
    step_dimension = step
    with open(mid_name_file, 'r') as f:
        while True:
            f.seek(int(step), 0)  # absolute position
            # f.seek(int(step), 1)  # relative position
            seek_to(f, '\n')
            row = parse_row(f.readline())
            row_id = row[0]
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


def get_rows_in_range(start_range, end_range):
    # rows_list = []
    with open(mid_name_file, "rt") as f:
        for line in f:
            current_id = line.split('\t')[0]
            if start_range <= current_id <= end_range:
                print line
    #             entity_id, entity_name, entity_type = line.replace('\n', '').split('\t')
    #             rows_list.append((entity_id, entity_name, entity_type))
    # return rows_list
