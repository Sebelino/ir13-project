import urlparse

__author__ = 'Daan Wynen'

import urllib2
from BeautifulSoup import BeautifulSoup
import html2text
import ImageDocument


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

if __name__=='__main__':
    s = Scraper('http://www.csc.kth.se/utbildning/kth/kurser/DD2427/')
    for i in s.get_documents():
        print(i.url)