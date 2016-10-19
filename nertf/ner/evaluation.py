from model import NERModel


def evaluate_model(test_filepath, ner_model_filepath, w2v_reader_file, batch_gen_file):
    sentence_num = 0
    nb_total_correct = 0
    nb_total_correct_entity = 0
    nb_total_error = 0
    nb_total_error_entity = 0
    words, tags = [], []

    ner_model = NERModel()
    ner_model.load(ner_model_filepath, w2v_reader_file, batch_gen_file)

    with open(test_filepath, 'r') as f:
        for line in f:
            if line != '\n':
                word, tag = line.replace('\n', '').split('\t')
                words.append(word)
                tags.append(tag)
            else:
                sentence_num += 1

                nb_correct = 0
                nb_correct_entity = 0
                nb_error = 0
                nb_error_entity = 0

                sentence = ' '.join(words)

                predicted_tags = ner_model.predict_sentence(sentence)

                # zip ok if lists not so big
                for correct, predicted in zip(tags, predicted_tags):
                    if correct == predicted:
                        nb_correct += 1
                        if correct != 'NIL' and correct != 'O':
                            nb_correct_entity += 1
                    else:
                        nb_error += 1
                        if correct != 'NIL' and correct != 'O':
                            nb_error_entity += 1

                words = []
                tags = []

                nb_total_correct += nb_correct
                nb_total_correct_entity += nb_correct_entity
                nb_total_error += nb_error
                nb_total_error_entity += nb_error_entity

                if sentence_num % 100 == 0:
                    print(
                        'Correct: {}\nCorrect Entities: {}\nErrors: {}\nErrors Entities: {}\nTotal: {}\n'.format(
                            nb_total_correct, nb_correct_entity, nb_total_error, nb_total_error_entity, sentence_num))
