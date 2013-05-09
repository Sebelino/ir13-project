__author__ = 'Oskar Bodemyr'


#import pysolr
import sunburnt
from ImageDocument import ImageDocument

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
	def __init__(self, solraddr = 'http://localhost:8080/solr/'):
		self.solr_interface = sunburnt.SolrInterface(solraddr)
		#self.solr = pysolr.Solr(solraddr, timeout=10)

	def simple_search(self, term):
		"""
		Simply search for a term and look for it in solr
		"""
		#return self.solr.search(term)
		return self.solr_interface.query(surrounding_text=term).execute()

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
		self.solr_interface.delete(imageurl)

	def doc_add(self, doc):
		"""
		Add a document to solr
		"""
		tempdict = self.solr_interface.query(url=doc.url).execute()

		if len(tempdict) == 0:
			self.solr_interface.add(doc)
			self.solr_interface.commit()

		else:
			doc2 = ImageDocument.from_dictionary(tempdict[0])
			if not doc.source_urls[0] in doc2.source_urls:
				doc.merge(doc2)
				self.solr_interface.add(doc)
				self.solr_interface.commit()
		self.solr_interface.commit()


		

# todo: a lot

if __name__ == '__main__': 
	q = Query('http://localhost:8080/solr/test2')

	doc1 = ImageDocument("testurl", ["tsource_url1"], ["text1"], ["description1"], ["title1"])
	q.doc_add(doc1)
	doc2 = ImageDocument("testurl", ["source_url3"], ["text3"], ["description3"], ["titel3"])
	q.doc_add(doc2)