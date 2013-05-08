import Document_Pickler
from Query import Query

q = Query('http://localhost:8080/solr/test2');
docs = Document_Pickler.retrieve_saved_documents();
for doc in docs:
	q.doc_add(doc)

