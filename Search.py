__author__ = 'Oskar Bodemyr'

import pysolr

class Search:
	def __init__(self, solraddr):
		self.solr = pysolr.Solr(solraddr, timeout=10)
	def search(self, term):
		'''
		Search using the requestHandler named imageSearch.
		If the requestHandler works, so should this query
		'''
		return self.solr.search(term,**{
			'qt':'imageSearch',
			})

if __name__ == '__main__': 
	s = Search('http://localhost:8080/solr/test3/')
	input = ""
	while(input != "exit"):
		input = raw_input("What would you like to search for? (exit-command: exit)\n>")
		results = s.search(input);
		print str(len(results)) + " results"
		for res in results:
			print format(res['url'])
