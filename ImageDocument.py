__author__ = 'Daan Wynen'


class ImageDocument:
    """
    This is what is called a document in the information retrieval context.
    in our case this is an image, identified by its URL and stored together with
    some information about the image like captions or alttexts used etc.
    """

    url = ''

    # how much text will be in this string depends on the scraper
    surrounding_text = ''

    # image can be used in different contexts
    #self.captions = []

    # same as for captions
    #self.alt_texts = []

    # todo: the structure of this data needs to be determined.
    # also, it needs to be clear which dat
    def __init__(self, url, text):
        self.url = url
        self.surrounding_text = text
