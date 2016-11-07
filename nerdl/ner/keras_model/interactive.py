import sys
import time

from model import NERModel
from nerdl.ner.w2v.word2vec_reader import Word2VecReader


def run_interactive_session(word2vec_filepath, training_filepath, model_filepath):
    print('>> Loading word2vec...')
    start = time.clock()
    word2vec_reader = Word2VecReader(word2vec_filepath, training_filepath)
    end = time.clock()
    print('<< Loaded word2vec in {} seconds.\n'.format(str(end - start)))

    print('>> Loading model...')
    start = time.clock()
    ner_model = NERModel(word2vec_reader)
    ner_model.load(model_filepath)
    end = time.clock()
    print('<< Loaded model in {} seconds.\n'.format(str(end - start)))

    while True:
        try:
            print('>> Type a query (type "exit" to exit):')
            input_string = raw_input().strip()
            # input_string = input('>> Type a query (type "exit" to exit):\n').strip()
            print('')
        except EOFError as e:
            print(e.message)
            sys.exit(0)

        if input_string == 'exit':
            break
        elif not input_string:
            print('>> Enter not empty sentence!')
            continue
        else:
            sentence = input_string.split()

            prediction = ner_model.predict_sentence(sentence)

            for ix in xrange(len(sentence)):
                print('{}\t{}'.format(sentence[ix], prediction[ix]))
            print('')
