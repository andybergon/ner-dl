import socket


class FigerSocket:
    def __init__(self):
        self.figer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.figer_socket.connect(("localhost", 5000))

    def request_prediction(self, sentence, recv_byte=2048, debug=0):
        sentence += '\n'  # needed for TCP protocol

        self.figer_socket.send(sentence)
        if debug != 0:
            print('Sent: {}'.format(sentence))

        response = self.figer_socket.recv(recv_byte)
        if debug != 0:
            print('Received: {}'.format(response))

        response = response[2:]  # trims strange char at start
        formatted_prediction = format_prediction(response)

        return formatted_prediction

    def close(self):
        self.figer_socket.close()


def format_prediction(prediction):
    formatted_prediction = []
    word_tags_scores = prediction.split('\n')

    for pair in word_tags_scores:
        word, tags_scores = pair.split('\t')
        tags_scores_formatted = []

        for tag_score in tags_scores.split(','):
            if tag_score == '':
                tag = 'O'
                score = 1.0
            else:
                tag, score = tag_score.split('@')
                tag = tag.replace('/', '', 1)
                tag = tag.replace('/', '.')
                tag = tag.upper()

            tags_scores_formatted.append((tag,score))

        formatted_prediction.append((word, tags_scores_formatted))

    return formatted_prediction
