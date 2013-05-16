from Scraper import Scraper
from mechanize import Browser
import ImageDocument
import random


__author__ = 'Tryti'

WIKIPEDIA_EN_RANDOM = 'en.wikipedia.org/wiki/Special:Random'
MAXSCRAPES = 10

class Crawler:
    def __init__(self, headurl, maxnr=MAXSCRAPES):
        """
        Starts to crawl from the headurl and continues at random
        """
        self.visited = []
        self.maxnr = maxnr
        self.next_link = headurl

    def crawl(self):
        #This is the browser we use
        self.br = Browser()

        scraped = 0
        #Scrape untill we scraped wanted amount or we fall into a sink
        while (scraped < self.maxnr) and (self.next_link):
            #Get page contents with Browser
            self.br.open(self.next_link)
            #And add it to the visited list
            self.visited.append(self.next_link)

            #if its html then we wants to scrape it
            if self.br.viewing_html() :
                #Get the imageDocuments on the site
                s = Scraper(self.br.response().read(), self.next_link)
                image_documents = s.get_image_documents()

                for i in image_documents:
                    yield i
                scraped+=1
            
            next_links = []
            #Get the links from the site and add them to the 
            for i in self.br.links(url_regex='http'):
                if (i.url != '#page'):
                    next_links.append(i.url)

            self.next_link = None

            #Unless we are at a sink we wants to continue
            if(len(next_links) != 0):
                while not self.next_link:
                    temp_link = self.random_link(next_links)
                    if (temp_link in self.visited):
                        self.next_link = None
                    else:
                        self.next_link = temp_link
    
        self.br.close() 

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

