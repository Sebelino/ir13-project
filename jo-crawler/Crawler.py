from Scraper import Scraper
from Scraper import WikipediaScraper
from mechanize import Browser
import ImageDocument
import random


__author__ = 'Tryti'

WIKIPEDIA_EN_RANDOM = 'en.wikipedia.org/wiki/Special:Random'
MAXSCRAPES = 10

class Crawler:
	def __init__(self, headurl, maxnr=MAXSCRAPES):
		'''
		Starts to crawl from the headurl and continues at random
		'''

		#This is the browser we use
		self.br = Browser()

		self.imageDocuments = []
		scraped = 0
		self.links = [headurl]
		self.visited = []

		#Scrape untill we scraped wanted amount or we fall into a sink
		while (scraped < maxnr) and (len(self.links) != 0):
			#Start scraping the site
			temp_url = self.links.pop(random.randint(0, len(self.links)-1))
			if not (temp_url in self.visited):
				self.visited.append(temp_url)
				self.scrape(temp_url)

				scraped+=1

		self.br.close()

	def scrape(self, url):
		#Get page contents with Browser
		self.br.open(url)
		if self.br.viewing_html():
			#Get the imageDocuments on the site
			scraper = Scraper(self.br.response().read(), url)
			newImages = scraper.get_image_documents()
			self.imageDocuments += newImages
			#Get the links from the site and add them to the 
			for i in self.br.links(url_regex='http'):
				if (i.url != '#page'):
					self.links.append(i.url)			


def main():
	test()

def test():
	url = 'http://www.xkcd.com'
	print('Starting test crawler on ' + url)

	c = Crawler(url)

	print('')
	print('Found these images')
	for i in c.imageDocuments:
		print(i.url)

if __name__ == '__main__':
    main()

