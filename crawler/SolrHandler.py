#! /usr/bin/env python2.7

__author__ = 'Oskar Bodemyr'

import GlobalConfiguration
import sunburnt
from ImageDocument import ImageDocument


class SolrHandler:
	"""
	Query-class for searching in solr. (Just trying pysolr really...)
	"""
	def __init__(self, solraddr = GlobalConfiguration.DEFAULT_SOLR_URL):
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
	q = SolrHandler('http://localhost:8080/solr/test3')

	doc1 = ImageDocument("testurl", ["tsource_url1"], ["text1"], ["description1"], ["title1"], ['keyword2'], 102, 104)
	q.doc_add(doc1)
	doc2 = ImageDocument("testurl", ["source_url3"], ["text3"], ["description3"], ["titel3"], ['keyword1'], 12, 14)
	q.doc_add(doc2)