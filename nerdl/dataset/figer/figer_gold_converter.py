from settings import path_settings

figer_gold_fp = path_settings.FIGER_GOLD_FILE

figer_gold_bio_fp = path_settings.FIGER_GOLD_BIO_FILE
figer_gold_not_bio_fp = path_settings.FIGER_GOLD_NOT_BIO_FILE


def convert_figer_gold_to_bio():
    with open(figer_gold_fp, 'r') as in_f, open(figer_gold_bio_fp, 'w+') as out_f:
        for line in in_f:
            if line != '\t\n' and line != '\n':
                word, tags = line.rstrip().split('\t')

                if tags != 'O':
                    bio, tags = tags.split('-', 1)
                    tags = tags.replace('/', '', 1).replace(',/', ',').replace('/', '.')
                    tags = bio + '-' + tags

                out_f.write(word + '\t' + tags + '\n')
            else:
                out_f.write('\n')


def convert_figer_gold_to_not_bio():
    with open(figer_gold_fp, 'r') as in_f, open(figer_gold_not_bio_fp, 'w+') as out_f:
        for line in in_f:
            if line != '\t\n' and line != '\n':
                word, tags = line.rstrip().split('\t')

                if tags != 'O':
                    bio, tags = tags.split('-', 1)
                    tags = tags.replace('/', '', 1).replace(',/', ',').replace('/', '.')

                out_f.write(word + '\t' + tags + '\n')
            else:
                out_f.write('\n')
