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
    surrounding_texts = []

    # image can be used in different contexts.
    # every context can have an alt text, a caption or thelike.
    # all these strings go in here, concatenated, as one description
    descriptions = []

    # titles of the pages the image was found on
    page_titles = []

    # keywords
    keywords = []

    def __init__(self, url, source_urls, surrounding_texts, descriptions, page_titles, keywords):
        self.url = url
        self.source_urls = source_urls
        self.surrounding_texts = surrounding_texts
        self.descriptions = descriptions
        self.page_titles = page_titles
        self.keywords = keywords

    @classmethod
    def from_dictionary(cls, d):
        s = Struct(**d)
        source_urls = list(s.source_urls)
        page_titles = list(s.page_titles)
        url = s.url
        descriptions= list(s.descriptions)
        surrounding_texts = list(s.surrounding_texts)
        keywords = list(s.keywords)
        return cls(url, source_urls, surrounding_texts, descriptions, page_titles, keywords)
        
    def merge(self, otherDoc):
        self.source_urls += otherDoc.source_urls
        self.page_titles += otherDoc.page_titles
        self.surrounding_texts += otherDoc.surrounding_texts
        self.descriptions += otherDoc.description
        self.keywords += otherDoc.keywords


class Struct:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

