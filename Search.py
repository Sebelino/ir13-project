__author__ = 'Oskar Bodemyr'

import pysolr
import logging

import GlobalConfiguration

log = logging.getLogger(__name__)


class Search:
    def __init__(self, solraddr):
        self.solr = pysolr.Solr(solraddr, timeout=10)

    def search(self, term):
        """Search using the requestHandler named imageSearch.
        If the requestHandler works, so should this query"""
        return self.solr.search(term, **{
            'qt': 'imageSearch',
        })


if __name__ == '__main__':
    s = Search('http://localhost:8080/solr/test3/')
    querystring = ""
    while querystring != "exit":
        querystring = raw_input("What would you like to search for? (exit-command: exit)\n>")
        results = s.search(querystring)
        log.info("%d results", len(results))
        for res in results.docs:
            log.info("%s", res['url'])
