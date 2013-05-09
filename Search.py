__author__ = 'Oskar Bodemyr'

import pysolr

class Search:
	def __init__(self, solraddr='http://localhost:8080/solr'):
		self.solr = pysolr.Solr(solraddr, timeout=10)
	def search(self, term):
		return self.solr.search(term, **{
			'qt':'imageSearch',
			})

if __name__ == '__main__': 
	s = Search('http://localhost:8080/solr/test3')
	res = s.search('anything');
	print res