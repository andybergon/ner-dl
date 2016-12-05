from tagger import Tagger


class CwLowSlashCwLowPointTagger(Tagger):
    def __init__(self):
        pass

    def tag(self, cwup_types):
        cwlow_types = self.convert_lowslash_to_lowpoint(cwup_types)
        return cwlow_types

    def convert_lowslash_to_lowpoint(self, cwslash_types):
        """

        :param cwslash_types: cw lowercase slash for hierarchy e.g. ['/common/topic', '/book/book']
        :return: e.g. cw lowercase point for hierarchy e.g. ['common.topic', 'book.book']
        """
        cwpoint_types = []

        for cwslash_type in cwslash_types:
            if cwslash_type == 'O':
                cwpoint_type = 'O'
            else:
                cwpoint_type = cwslash_type.replace('/', '', 1).replace('/', '.')

            cwpoint_types.append(cwpoint_type)

        cwpoint_types = set(cwpoint_types)

        return cwpoint_types
