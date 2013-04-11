__author__ = 'Oskar Bodemyr'


import pysolr

class Query:
	"""
	Query-class for searching in solr. (Just trying pysolr really...)
	"""
	def __init__(self, solraddr = 'http://localhost:8983/solr/'):
		self.solr = pysolr.Solr(solraddr, timeout=10)

	def simple_search(self, term):
		"""
		Simply search for a term and look for it in solr
		"""
		return self.solr.search(term)

# todo: everything

if __name__ == '__main__':
	q = Query('http://localhost:8983/solr/')
	for res in q.simple_search('Dell'):
		print(res['name'])