class Tagger:
    def __init__(self):
        pass

    def tag_string(self, tag_string, remove_bi_tag=False):
        if 'O' == tag_string:
            return tag_string
        elif 'B-' in tag_string or 'I-' in tag_string:
            bio, tags = tag_string.split('-', 1)
            tags = tags.split(',')
            tags = self.tag(tags)
            if remove_bi_tag:
                complete_tags_string = ','.join(tags)
            else:
                complete_tags_string = bio + '-' + ','.join(tags)
        else:
            tags = tag_string.split(',')
            tags = self.tag(tags)
            complete_tags_string = ','.join(tags)

        return complete_tags_string

    def tag(self, entity_types):
        """

        :param entity_types: list [A, B, C]
        :return: list [A1, B1]
        """
        raise NotImplementedError("Subclass must implement abstract method")
