__author__ = 'Daan Wynen'


class ImageDocument:
    """
    This is what is called a document in the information retrieval context.
    in our case this is an image, identified by its URL and stored together with
    some information about the image like captions or alttexts used etc.
    """

    url = ''

    # urls of the pages this image was found on
    source_urls = []

    # how much text will be in this string depends on the scraper
    surrounding_text = []

    # image can be used in different contexts.
    # every context can have an alt text, a caption or thelike.
    # all these strings go in here, concatenated, as one description
    description = []

    # titles of the pages the image was found on
    page_titles = []

    # todo: the structure of this data needs to be determined.
    # also, it needs to be clear which data
    def __init__(self, url, source_urls, surrounding_text, description, page_titles):
        self.url = url
        self.source_urls = source_urls
        self.surrounding_text = surrounding_text
        self.description = description
        self.page_titles = page_titles

    @classmethod
    def from_dictionary(cls, d):
        s = Struct(**d)
        source_urls = list(s.source_urls)
        page_titles = list(s.page_titles)
        url = s.url
        description = list(s.description)
        surrounding_text = list(s.surrounding_text)
        return cls(url, source_urls, surrounding_text, description, page_titles)
        
    def merge(self, otherDoc):
        self.source_urls += otherDoc.source_urls
        self.page_titles += otherDoc.page_titles
        self.surrounding_text += otherDoc.surrounding_text
        self.description += otherDoc.description

class Struct:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

