import sys


def run_interactive_session(ner_model):
    while True:
        try:
            print('>> Type a query (type "exit" to exit):')
            input_string = raw_input().strip()  # TODO: split in sentences if > max_char_in_sentence
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
            prediction = ner_model.predict_sentence(input_string)

            for ix in xrange(len(input_string)):
                print('{}\t{}'.format(input_string[ix], prediction[ix]))
            print('')
