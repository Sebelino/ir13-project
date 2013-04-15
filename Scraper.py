# /usr/bin/env python

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

SURROUNDINGSIZE_THRESHOLD = 200

BROWSER_USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0"


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
        """
        result = []
        imgs = self.soup.findAll("img")

        print("found {0} <img> tags on the page.".format(len(imgs)))
        
        for image_node in imgs:
            full_url = urlparse.urljoin(self.url, image_node["src"])

            if self.should_ignore(full_url):
                continue
            
            t = self.extract_surrounding_text(image_node)
            caption = self.extract_caption(image_node)
            alt_text = self.extract_alttext(image_node)
            im_doc = ImageDocument.ImageDocument(full_url, self.url, t)
            if caption:
                im_doc.description = caption
                if alt_text:
                    im_doc += " "+alt_text
            elif alt_text:
                im_doc.description = alt_text
            title = self.extract_title(image_node)

            result.append(im_doc)

        return result


    def extract_title(self, image_node):
        # leave this to wikiscraper where we know hot to do this.
        # for now at least
        pass
        
    
    def extract_surrounding_text(self, image_node):
        """
        @type image_node: Node
        """
        text_node = image_node
        
        while text_node!=self.soup:
            text_node = text_node.parent
            text = text_node.renderContents(None)
            text = html2text.html2text(text)
            if len(text.split()) >= SURROUNDINGSIZE_THRESHOLD:
                print('length of surrounding_text: {0}'.format(len(text.split())))
                return text            

        # we hit the root node, there will be no more text to index...
        return text

        
    def extract_caption(self, img):
        # don't try to find captions in random pages for now,
        # leave that to the wikipedia scraper
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
    def __init__(self, url=WIKIPEDIA_EN_RANDOM):

        if url==WIKIPEDIA_EN_RANDOM:
            print('visit random wikipedia page')
    
        req = urllib2.Request(url, headers={'User-Agent': BROWSER_USER_AGENT})
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

        # also save a stripped down version for indexing.
        self.plaintext = html2text.html2text(self.full_text)

        #print(self.plaintext)

    def extract_caption(self, image_node):

        print("extracting image caption from wikipedia image")
    
        while (not dict(image_node.attrs).has_key('class') \
          or image_node['class']!='thumbinner')\
          and image_node.parent!=None:
            image_node = image_node.parent

        # this probably means we didn't find a proper image but some icon
        # and then we navigated up to the document root aaaannnd... well...
        # let's pretend nobody saw that... :D
        if image_node is None or image_node.parent==None:
            return None

        n=image_node.find('div', {'class':'thumbcaption'})
        if not n:
            return None
        
        # most (all?) wikipedia image captions have this annoying magnify link...
        m=n.find('div', {'class':'magnify'})
        if m:
            m.replaceWith("")

        return html2text.html2text(n.renderContents(None))


def main():
    print('scraping ONE page')
    # s = Scraper('http://www.csc.kth.se/utbildning/kth/kurser/DD2427/')
    #s = WikipediaScraper('http://en.wikipedia.org/wiki/Brooklyn_Technical_High_School')
    s= WikipediaScraper()
    for i in s.get_documents():
        print('\n\n===============================================')
        print(i.url)
        print(i.source_urls[0])
        print(i.surrounding_text)
        print(i.description)
        print(i.title)
     
        
if __name__ == '__main__':
    main()
else:
    print('loaded, but not in __main__')
