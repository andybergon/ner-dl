from tagger import Tagger


class CwUpPointCwLowPointTagger(Tagger):
    def __init__(self):
        pass

    def tag(self, cwup_types):
        cwlow_types = self.convert_cwup_to_cwlow(cwup_types)
        return cwlow_types

    def convert_cwup_to_cwlow(self, cwup_types):
        """

        :param cwup_types: cw uppercase point for hierarchy e.g. [AWARD.AWARD, MUSIC.ALBUM]
        :return: e.g. cw lowercase point for hierarchy e.g. [award.award, music.album]
        """
        cwlow_types = []

        for cwup_type in cwup_types:
            if cwup_type == 'O':
                cwlow_type = 'O'
            else:
                cwlow_type = cwup_type.lower()

            cwlow_types.append(cwlow_type)

        cwlow_types = set(cwlow_types)

        return cwlow_types
