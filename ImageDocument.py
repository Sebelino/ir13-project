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
    surrounding_text = ''

    # image can be used in different contexts.
    # every context can have an alt text, a caption or thelike.
    # all these strings go in here, concatenated, as one description
    description = ''

    # title of the image
    # if an image has a separate title then this is very likely to
    # contain a lot of information about the image's content
    title = ''

    # titles of the pages the image was found on
    page_titles = []

    # todo: the structure of this data needs to be determined.
    # also, it needs to be clear which data
    def __init__(self, url, source_url, text, page_title, keywords):
        self.url = url
        self.source_urls = [source_url]
        self.surrounding_text = text
        self.page_titles.append(page_title)
        self.keywords = keywords


