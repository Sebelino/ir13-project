#! /usr/bin/env python2.7

import logging
import DocumentPickler
from SolrHandler import SolrHandler
import GlobalConfiguration

log = logging.getLogger(__name__)

q = SolrHandler('http://localhost:8080/solr/test3')

docs = DocumentPickler.retrieve_saved_documents()

for idx, doc in enumerate(docs):
    q.doc_add(doc)
    if (idx+1)%100==0:
        log.info('successfully inserted document no. {0}'.format(idx + 1))
    else:
        log.debug('successfully inserted document no. {0}'.format(idx + 1))


