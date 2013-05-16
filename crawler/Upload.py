#! /usr/bin/env python2.7

import logging
import sys
import traceback
from SolrHandler import SolrHandler
import GlobalConfiguration
from Crawler import Crawler

log = logging.getLogger(__name__)

q = SolrHandler(GlobalConfiguration.DEFAULT_SOLR_URL)


def scrape_documents(min_count=0):

    doc_count = 0

    s = Crawler()
    docs = s.crawl(min_count)

    while min_count <= 0 or doc_count < min_count:
        for doc in docs:
            log.debug('uploaded image doc from %s', doc.url)
            doc_count += 1
            if doc_count % 100 == 0:
                log.info('%d images and counting...', doc_count)
            yield doc


documents = scrape_documents()
for idx, doc in enumerate(documents):
    print('hello')
    try:
        q.doc_add(doc)

    except KeyboardInterrupt:
        sys.exit(0)
    except:
        log.debug(traceback.format_exc())
        sys.exc_clear()

    if (idx+1)%100==0:
        log.info('successfully inserted document no. %d from %s', idx+1, doc.url)
    else:
        log.debug('successfully inserted document no. %d from %s', idx+1, doc.url)


