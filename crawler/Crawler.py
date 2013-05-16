import cookielib
import logging
import sys
import traceback
from Scraper import Scraper
import mechanize
import ImageDocument
import random
import GlobalConfiguration

log = logging.getLogger(__name__)


__author__ = 'Tryti'

WIKIPEDIA_EN_RANDOM = 'en.wikipedia.org/wiki/Special:Random'
MAXSCRAPES = 10
USER_AGENT = 'Mozilla/21.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/21'


class Crawler:
    def __init__(self, url_seeds=GlobalConfiguration.DEFAULT_URL_SEEDS):
        """
        Starts to crawl from the headurl and continues at random
        """
        self.visited = []
        self.url_seeds = url_seeds
        self.next_link = self.get_random_url_seed()

    def get_random_url_seed(self):
        return self.url_seeds[random.randint(0, len(self.url_seeds)-1)]

    def get_browser(self):
        # shamelessly stolen from http://stockrt.github.io/p/emulating-a-browser-in-python-with-mechanize/

        # Browser
        br = mechanize.Browser()

        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)

        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Want debugging messages?
        # br.set_debug_http(True)
        # br.set_debug_redirects(True)
        # br.set_debug_responses(True)

        # User-Agent (this is cheating, ok?)
        br.addheaders = [('User-agent', USER_AGENT)]

        seed = self.get_random_url_seed()
        log.debug('initializing browser to %s', seed)
        self.br = br
        self.br.open(seed)

        return br

    def crawl(self, maxnr=MAXSCRAPES):

        scraped = 0
        #Scrape until we scraped wanted amount or we fall into a sink
        while maxnr <= 0 or scraped < maxnr:

            try:

                self.br = self.get_browser()
                log.debug('scraping %s', self.next_link)
                #Get page contents with Browser
                self.br.open(self.next_link)
                #And add it to the visited list
                if self.next_link not in self.url_seeds:
                    self.visited.append(self.next_link)
                    if self.br.viewing_html() :
                        #Get the imageDocuments on the site
                        s = Scraper(self.br.response().read(), self.next_link)
                        image_documents = s.get_image_documents()

                        for i in image_documents:
                            yield i
                        scraped += 1

                next_links = []
                #Get the links from the site and add them to the
                for i in self.br.links(url_regex='http'):
                    if i.url != '#page':
                        next_links.append(i.url)

                self.next_link = None

                #Unless we are at a sink we wants to continue
                if len(next_links) != 0:
                    random.shuffle(next_links)
                    for temp_link in next_links:
                        if temp_link not in self.visited:
                            self.next_link = temp_link
                            break
            except:
                log.debug(traceback.format_exc())
                sys.exc_clear()
                try:
                    self.br.close()
                except:
                    pass

        try:
            log.debug(traceback.format_exc())
            sys.exc_clear()
            self.br.close()
        except:
            pass

    def random_link(self, links):
        return links.pop(random.randint(0, len(links)-1))



def main():
    test()

def test():
    url = 'http://www.xkcd.com'
    print('Starting test crawler on ' + url)

    c = Crawler(url)

    print('')
    print('Found these images')
    for i in c.crawl():
        print(i.url)

if __name__ == '__main__':
    main()

