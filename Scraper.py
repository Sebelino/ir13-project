#! /usr/bin/env python

# -*- coding: utf-8 -*-

__author__ = 'Daan Wynen'

import urllib2
import urlparse
from BeautifulSoup import BeautifulSoup
import MLStripper
import ImageDocument
import Keywords

WIKIPEDIA_EN_RANDOM = 'http://en.wikipedia.org/wiki/Special:Random'

BLACKLIST = [
    'upload.wikimedia.org/wikipedia/commons/thumb/5/55/WMA_button2b.png/17px-WMA_button2b.png',
    'bits.wikimedia.org',
    '/Question_book-new.svg/',
    '/thumb/b/ba/Flag_of_New_York_City.svg/',
    'thumb/4/4a/Commons-logo.svg',
    'Disambig_gray.svg.png'
]

SURROUNDING_TEXT_TARGET = 200

BROWSER_USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0"


class Scraper:
    def __init__(self, url):
        self.url = url

        req = urllib2.Request(url, headers={'User-Agent': BROWSER_USER_AGENT})
        site = urllib2.urlopen(req)
        content = site.read()
        self.url = site.geturl()
        if url != self.url:
            print("was redirected to {0}".format(self.url))

        site.close()

        # build the soup first.
        # this lets us use its encoding detection mechanism to decode the page's content.
        self.soup = self.get_relevant_root(BeautifulSoup(content))

        title_tag = self.soup.find('title')
        if title_tag:
            self.page_title = title_tag.renderContents(None)
        else:
            self.page_title = ''

        # save the raw html of the page but as unicode
        self.full_text = self.soup.renderContents(None)

        # also save a stripped down version for indexing.
        self.plaintext = self.strip_html(self.full_text)

    def get_relevant_root(self, soup):
        return soup

    def strip_html(self, html):
        result = MLStripper.strip_tags(html)
        return result

    def get_documents(self):
        """
        Returns every image document for this page.
        """
        imgs = self.soup.findAll("img")

        print("Found {0} <img> tags on the page.".format(len(imgs)))

        # replace all images by their respective urls
        for image_node in imgs:
            image_node.replaceWith(image_node["src"])

        flat_text = self.strip_html(self.soup.renderContents(None))

        result = []
        for image_node in imgs:
            full_url = urlparse.urljoin(self.url, image_node["src"])

            if self.should_ignore(full_url):
                continue

            surrounding_text = self.extract_surrounding_text(image_node, flat_text)
            caption = self.extract_caption(image_node)
            alt_text = self.extract_alttext(image_node)

            keywords = Keywords.extract_keywords_grammar(surrounding_text)

            im_doc = ImageDocument.ImageDocument(full_url, self.url, surrounding_text, self.page_title, keywords)

            if caption:
                im_doc.description = caption
                if alt_text:
                    im_doc += " " + alt_text
            elif alt_text:
                im_doc.description = alt_text

            result.append(im_doc)

        return result

    def extract_surrounding_text(self, image_node, flat_text):
        """
        @type image_node: Node
        """

        current_url = image_node['src']

        components = flat_text.split(current_url)

        # get teh text preceding and following the image
        # this will discard information if the url occurred more than once.
        # we don't like that so we pretend it didn't happen...
        (pre, post) = components[0], components[1]

        # split both
        (pre, post) = pre.split(), post.split()

        # how many words can we take from pre component
        pre_len = min(len(pre), SURROUNDING_TEXT_TARGET/2)

        # same for post component
        post_len = min(len(post), SURROUNDING_TEXT_TARGET/2)

        result_wordlist = pre[-pre_len:] + post[:post_len]

        # make a regular text from our words
        result = ' '.join(result_wordlist)

        return result

    def extract_caption(self, img):
        # don't try to find captions in random pages for now,
        # leave that to the WikipediaScraper
        return None

    def extract_alttext(self, img):
        try:
            return img['alt']
        except:
            return None

    def should_ignore(self, url):
        for string in BLACKLIST:
            if url.find(string) != -1:
                return True
        return False


class WikipediaScraper(Scraper):

    def get_relevant_root(self, soup):
        return soup.find('div', {"id": "content"})

    def __init__(self, url=WIKIPEDIA_EN_RANDOM):
        if url == WIKIPEDIA_EN_RANDOM:
            print('visit random wikipedia page')
        Scraper.__init__(self, url)

    def extract_caption(self, image_node):

        print("extracting image caption from wikipedia image")

        while (not dict(image_node.attrs).has_key('class') \
                   or image_node['class'] != 'thumbinner') \
            and image_node.parent is not None:
            image_node = image_node.parent

        # this probably means we didn't find a proper image but some icon
        # and then we navigated up to the document root aaaannnd... well...
        # let's pretend nobody saw that... :D
        if image_node is None or image_node.parent == None:
            return None

        n = image_node.find('div', {'class': 'thumbcaption'})
        if not n:
            return None

        # most (all?) wikipedia image captions have this annoying magnify link...
        m = n.find('div', {'class': 'magnify'})
        if m:
            m.replaceWith("")

        return MLStripper.strip_tags(n.renderContents(None))


def main():
    print('scraping ONE page')
    # s = Scraper('http://en.wikipedia.org/wiki/Brooklyn_Technical_High_School')
    # s = Scraper('http://www.csc.kth.se/utbildning/kth/kurser/DD2427/')
    # return
    #s = WikipediaScraper('http://en.wikipedia.org/wiki/Brooklyn_Technical_High_School')
    s = WikipediaScraper()
    for i in s.get_documents():
        print('\n\n===============================================')
        print('Url: {0}'.format(i.url))
        print('Source url: {0}'.format(i.source_urls[0]))
#        print('Image title: {0}'.format(i.title))
        print('page title: {0}'.format(i.page_titles[0]))
        print('Description: {0}'.format(i.description))
        print('Keywords: {0}'.format(';'.join(i.keywords)))
        print('==========================')
        print(i.surrounding_text.encode('utf-8', 'ignore'))
        print('===============================================\n\n')


if __name__ == '__main__':
    main()
else:
    print('loaded, but not in __main__')
