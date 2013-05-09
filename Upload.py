#! /usr/bin/env python2.7

import sys
from crawler import DocumentPickler

sys.path.append("./sunburnt")

from Query import Query

q = Query('http://localhost:8080/solr/test3')
docs = DocumentPickler.retrieve_saved_documents()
for idx, doc in enumerate(docs):
    q.doc_add(doc)
    print('successfully inserted document no. {0}'.format(idx + 1))

