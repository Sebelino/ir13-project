#! /usr/bin/env python

# -*- coding: utf-8 -*-

__author__ = 'Daan Wynen, Jo Tryti'

from BeautifulSoup import BeautifulSoup
from StringIO import StringIO
from PIL import Image
import urllib2
import urlparse

import MLStripper
import ImageDocument
import Keywords

#Constants
SURROUNDING_TEXT_TARGET = 200
MIN_IMAGE_SIZE = 100

class Scraper:
    def __init__(self, content=None, url=None):
        if url:
            self.url = url

        if content:
            #Build the soup
            self.soup = self.get_relevant_root(BeautifulSoup(content))
            #set the title
            title_tag = self.soup.find('title')
            if title_tag:
                self.page_title = title_tag.renderContents(None)
            else:
                self.page_title = ''

            # save the raw html of the page but as unicode
            self.full_text = self.soup.renderContents(None)

            # also save a stripped down version for indexing.
            self.plaintext = self.strip_html(self.full_text)


    def get_image_documents(self):
        """
        Returns the wanted image document form this page.
        """
        result = []
        if not self.soup:
            return result
        'TODO-does this work?'

        imgs = self.soup.findAll("img")

        # replace all images by their respective urls
        for image_node in imgs:
            image_node.replaceWith(image_node["src"])

        flat_text = self.strip_html(self.soup.renderContents(None))
        'TODO-use self.plaintext?'

        result = []
        for image_node in imgs:
            full_url = urlparse.urljoin(self.url, image_node["src"])

            if not self.check_image(full_url):
                continue

            surrounding_text = self.extract_surrounding_text(image_node, flat_text)
            caption = self.extract_caption(image_node)
            alt_text = self.extract_alttext(image_node)

            keywords = Keywords.extract_keywords_grammar(surrounding_text)

            description = ''
            if caption:
                description = caption
                if alt_text:
                    description += " " + alt_text
            elif alt_text:
                description = alt_text

            im_doc = ImageDocument.ImageDocument(
                url=full_url,
                source_urls=[self.url],
                surrounding_texts=[surrounding_text],
                descriptions=[description],
                page_titles=[self.page_title],
                keywords=keywords)

            result.append(im_doc)

        return result


    def check_image(self, img_url):
        '''
        returns true if we wants to index this image. Checks for image size and if it is a valid image format
        '''
        f = urllib2.urlopen(img_url)
        s = StringIO(f.read())
        image = Image.open(s)

        #First we need to check if the requested image is a real image
        'TODO-check image head'

        #Check if the image is smaler then our minimumsize to remove icons etc
        (w, h) = image.size

        if (w < MIN_IMAGE_SIZE) or (h < MIN_IMAGE_SIZE):
            #TO SMALL
            return False
        else:
            return True

    def extract_surrounding_text(self, image_node, flat_text):
        """
        @type image_node: Node
        """

        current_url = image_node['src']

        components = flat_text.split(current_url)

        # get teh text preceding and following the image
        # this will discard information if the url occurred more than once.
        # we don't like that so we pretend it didn't happen...
        if (len(components) > 1):
            (pre, post) = components[0], components[1]
        else:
            (pre, post) = components[0], ''

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
    def get_relevant_root(self, soup):
        #I dont get this
        return soup


    def strip_html(self, html):
        result = MLStripper.strip_tags(html)
        return result


class WikipediaScraper(Scraper):

    def get_relevant_root(self, soup):
        return soup.find('div', {"id": "content"})

    def extract_caption(self, image_node):

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
    print('No main for Scraper')

if __name__ == '__main__':
    main()
