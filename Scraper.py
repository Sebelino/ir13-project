import urlparse

__author__ = 'Daan Wynen'

import urllib2
from BeautifulSoup import BeautifulSoup
import html2text
import ImageDocument

WIKIPEDIA_EN_RANDOM = 'http://en.wikipedia.org/wiki/Special:Random'

BLACKLIST = [
    'upload.wikimedia.org/wikipedia/commons/thumb/5/55/WMA_button2b.png/17px-WMA_button2b.png',
    'bits.wikimedia.org',
    '/Question_book-new.svg/',
    '/thumb/b/ba/Flag_of_New_York_City.svg/'
    'thumb/4/4a/Commons-logo.svg'
]


class Scraper:
    def __init__(self, url):
        self.url = url

        site = urllib2.urlopen(url)
        content = site.read()
        site.close()

        # build the soup first.
        # this lets us use its encoding detection mechanism to decode the page's content.
        self.soup = BeautifulSoup(content)

        # save the raw html of the page but as unicode
        self.full_text = self.soup.renderContents(None)

        # lso save a stripped down version for indexing.
        self.plaintext = html2text.html2text(self.full_text)

        #print(self.plaintext)

    def get_documents(self):
        """
        Returns every image document for this page.
        todo: for now the surrounding text is just te complete website's plaintext.
        this should be done more cleverly...
        """
        image_urls = [urlparse.urljoin(self.url, image["src"]) for image in self.soup.findAll("img")]
        return [ImageDocument.ImageDocument(url, self.plaintext) for url in image_urls]


class WikipediaScraper:
    def __init__(self, url=WIKIPEDIA_EN_RANDOM):
        req = urllib2.Request(url, headers={
            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0"})
        site = urllib2.urlopen(req)
        self.url = site.geturl()
        if url != self.url:
            print("was redirected to {0}".format(self.url))
        content = site.read()
        site.close()

        # build the soup first.
        # this lets us use its encoding detection mechanism to decode the page's content.
        self.soup = BeautifulSoup(content)

        # main content is always stored in <div id="content" class="mw-body" role="main">
        self.soup = self.soup.find('div', {"id": "content"})

        # save the raw html of the page but as unicode
        self.full_text = self.soup.renderContents(None)

        # lso save a stripped down version for indexing.
        self.plaintext = html2text.html2text(self.full_text)

        #print(self.plaintext)

    def get_documents(self):
        """
        Returns every image document for this page.
        todo: for now the surrounding text is just te complete website's plaintext.
        this should be done more cleverly...
        """
        image_urls = [urlparse.urljoin(self.url, image["src"]) for image in self.soup.findAll("img")]
        return [ImageDocument.ImageDocument(url, self.plaintext) for url in image_urls if not self.should_ignore(url)]

    def should_ignore(self, url):
        for string in BLACKLIST:
            if url.find(string) != -1:
                return True
        return False


if __name__ == '__main__':
    # s = Scraper('http://www.csc.kth.se/utbildning/kth/kurser/DD2427/')
    s = WikipediaScraper('http://en.wikipedia.org/wiki/Brooklyn_Technical_High_School')
    for i in s.get_documents():
        print(i.url)