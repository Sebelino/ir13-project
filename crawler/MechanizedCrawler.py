from crawler import Scraper

__author__ = 'daan'

DEFAULT_URL_SEED = 'http://www.reddit.com/'

MAX_LINK_DEPTH = 30


class MechanizedCrawler:
    url_seed = DEFAULT_URL_SEED

    def __init__(self, url=None):
        if url:
            self.url_seed = url

        self.scraper = Scraper()


    def _get_new_website(self):

        # ... call meachanize

        next_html_text = ''

        yield next_html_text

    def get_image_documents(self):
        '''returns a generator for image documents'''

        #....
        docs=None
        for doc in docs:
            yield doc