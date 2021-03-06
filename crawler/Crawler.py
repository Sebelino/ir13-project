import cookielib
import logging
import re
import sys
import traceback
import urllib2
from Scraper import Scraper
import mechanize
import ImageDocument
import random
import GlobalConfiguration

log = logging.getLogger(__name__)


__author__ = 'Tryti'


gifre = re.compile('.*\\.gif.*')

WIKIPEDIA_EN_RANDOM = 'en.wikipedia.org/wiki/Special:Random'
MAXSCRAPES = 10
MAX_SCRAPES_PER_WALK = 15
USER_AGENT = 'Mozilla/21.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/21'



class Crawler:
    def __init__(self, url_seeds=GlobalConfiguration.DEFAULT_URL_SEEDS):
        """
        Starts to crawl from the headurl and continues at random
        """
        self.visited = []
        self.url_seeds = url_seeds

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
        br.set_handle_robots(True)

        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Want debugging messages?
        # br.set_debug_http(True)
        # br.set_debug_redirects(True)
        # br.set_debug_responses(True)

        # User-Agent (this is cheating, ok?)
        br.addheaders = [('User-agent', USER_AGENT)]

        seed = self.get_random_url_seed()
        log.info('seeding browser with %s', seed)
        br.open(seed)
        self.br = br

        # dont scrape the seed page...
        self.next_link = self.get_next_link()

        return br

    def get_next_link(self):

        next_links = []
        #Get the links from the site and add them to the
        for i in self.br.links(url_regex='http'):
            for regex in GlobalConfiguration.page_block_regexs:
                if regex.search(i.url):
                    log.debug('link %s not feasible for scraping.', i.url)
                    continue
            if i.url != '#page':
                next_links.append(i.url)

        self.next_link = None

        #Unless we are at a sink we wants to continue
        if len(next_links) != 0:
            random.shuffle(next_links)
            for temp_link in next_links:
                if temp_link not in self.visited:
                    return temp_link
        else:
            log.info('couldn\'t find link to follow.')
            raise RuntimeError

    def crawl(self, maxnr=MAXSCRAPES):

        scraped = 0
        #Scrape until we scraped wanted amount or we fall into a sink
        while maxnr <= 0 or scraped < maxnr:
            try:

                walked = 0

                self.br = self.get_browser()

                while maxnr <= 0 or scraped < maxnr:


                    #Get page contents with Browser
                    success=False
                    while not success:
                        try:
                            self.next_link = self.get_next_link()
                            self.br.open(self.next_link)
                            walked += 1
                            if walked > MAX_SCRAPES_PER_WALK:
                                log.info('maximum link steps reached, restarting at a root.')
                                raise RuntimeError
                            success = True
                        except urllib2.HTTPError:
                            log.debug(traceback.format_exc())
                            sys.exc_clear()
                            walked += 1
                            if walked > MAX_SCRAPES_PER_WALK:
                                log.info('maximum link steps reached, restarting at a root.')
                                raise RuntimeError
                            self.br.back()

                    log.debug('scraping %s', self.next_link)

                    #And add it to the visited list
                    if self.next_link not in self.url_seeds:
                        self.visited.append(self.next_link)
                        if self.br.viewing_html():
                            #Get the imageDocuments on the site
                            s = Scraper(self.br.response().read(), self.next_link)
                            image_documents = s.get_image_documents()

                            for i in image_documents:
                                yield i
                            scraped += 1
                        else:
                            self.br.back()

            except KeyboardInterrupt:
                return
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

        except KeyboardInterrupt:
            return
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

