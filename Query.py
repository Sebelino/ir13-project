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

	def optimize(self):
		"""
		Defragmentation (I think)
		"""
		self.solr.optimize()

	def delete(self, imageurl):
		"""
		Delete a document in solr by it's image url
		"""
		self.solr.delete(url=imageurl)

# todo: a lot

if __name__ == '__main__':
	q = Query('http://localhost:8983/solr/')
	while(True):
		term = raw_input('What do you want to search for?\n')
		for res in q.simple_search(term):
				print(res['name'])