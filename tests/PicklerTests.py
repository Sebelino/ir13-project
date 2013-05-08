#! /usr/bin/env python2.7
from numpy.lib.utils import source
import os

import DocumentPickler
import tempfile
from ImageDocument import ImageDocument


__author__ = 'daan'

import unittest


class DocumentPicklerTests(unittest.TestCase):

    def get_sample_documents(self):

        d1 = ImageDocument(
            url='someurl1',
            source_urls=['wikipage1', 'wikipage2'],
            surrounding_texts=['bla', 'foo'],
            descriptions=['foo', 'bar'],
            page_titles=['', 'title1'],
            keywords=['moo', 'milka'])

        d2 = ImageDocument(
            url='someurl2',
            source_urls=['wikipage1', 'wikipage3'],
            surrounding_texts=['beer', 'milk'],
            descriptions=['good', 'bad'],
            page_titles=['YAY', 'BOO'],
            keywords=['happy', 'sad'])

        d3 = ImageDocument(
            url='someurl31',
            source_urls=['wikipage3', 'wikipage2'],
            surrounding_texts=['studies', 'free time'],
            descriptions=['cool', 'coooooool'],
            page_titles=['how to spend a day on one bug', 'how to do nothing all day'],
            keywords=['dungeon', 'sun'])

        return [d1, d2, d3]

    def test_pickling_preserves_attributes(self):
        docs = self.get_sample_documents()
        (_, dumpfilename) = tempfile.mkstemp()

        DocumentPickler.save_documents(docs, dumpfilename)

        docs = DocumentPickler.retrieve_saved_documents(dumpfilename)

        os.remove(dumpfilename)

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
