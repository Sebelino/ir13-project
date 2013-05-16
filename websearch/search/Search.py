__author__ = 'Oskar Bodemyr'

import pysolr
import logging
import sys
sys.path.append("~/git/ir13-project")
import GlobalConfiguration

log = logging.getLogger(__name__)


class Search:
    def __init__(self, solraddr='http://130.229.171.104:8080/solr/test3'):
        self.solr = pysolr.Solr(solraddr, timeout=10)

    def search(self, term):
        """Search using the requestHandler named imageSearch.
        If the requestHandler works, so should this query"""
        list = []
        results = self.solr.search(term, qt='imageSearch', rows=100)
        for result in results:
            list.append(result['url'])
        return list


if __name__ == '__main__':
    s = Search()
    querystring = ""
    while querystring != "exit":
        querystring = raw_input("What would you like to search for? (exit-command: exit)\n>")
        results = s.search(querystring)
        log.info("%d results", len(results))
        for res in results:
            log.info("%s", res)
