#! /usr/bin/env python2.7
from ImageDocument import ImageDocument
from Scraper import WikipediaScraper

__author__ = 'daan'

import unittest


class WikipediaScraperTests(unittest.TestCase):

    def test_all_resulting_docs_have_all_attributes_set(self):
        for i in range(10):
            s = WikipediaScraper()
            docs = s.get_documents()
            for doc in docs:
                self.failUnless(isinstance(doc, ImageDocument))
                self.failUnless(doc.source_urls)
                self.failUnless(doc.page_titles)
                self.failUnless(doc.url)
                self.failUnless(doc.descriptions)
                self.failUnless(doc.surrounding_texts)
                self.failUnless(doc.keywords)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
