__author__ = 'Oskar Bodemyr'


#import pysolr
import sunburnt
import ImageDocument

class Document:
	"""
	Just a simple test class to use with the Solr example
	"""
	def __init__(self, nr, name, manu):
		self.id = nr
		self.sku = ""
		self.name = name
		self.manu = manu
		self.cat = ""
		self.features = ""
		self.includes = ""
		self.weight = 1.5
		self.price = 1234
		self.popularity = 15
		self.instock = True

class Query:
	"""
	Query-class for searching in solr. (Just trying pysolr really...)
	"""
	def __init__(self, solraddr = 'http://localhost:8983/solr/'):
		self.solr_interface = sunburnt.SolrInterface(solraddr)
		#self.solr = pysolr.Solr(solraddr, timeout=10)

	def simple_search(self, term):
		"""
		Simply search for a term and look for it in solr
		"""
		#return self.solr.search(term)
		return self.solr_interface.query(name=term).execute()

	def optimize(self):
		"""
		Defragmentation (I think)
		"""
		#old code for pysolr
		#self.solr.optimize()

	def delete(self, imageurl):
		"""
		Delete a document in solr by it's image url
		"""
		#old code from pysolr
		#self.solr.delete(url=imageurl)

	def doc_add(self, doc):
		"""
		Add a document to solr
		"""
		self.solr_interface.add(doc)
		self.solr_interface.commit()

# todo: a lot

if __name__ == '__main__': 
	q = Query('http://localhost:8983/solr/')
	doc = Document("1234ABC", "Dell Microwave Deluxe", "DELL")
	q.doc_add(doc)
	
	while(True):
		term = raw_input('What do you want to search for?\n')
		for res in q.simple_search(term):
			print res['name']