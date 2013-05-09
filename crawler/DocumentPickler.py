#! /usr/bin/env python2.7

import os
import pickle
import GlobalConfiguration
from crawler.Scraper import WikipediaScraper

MIN_DOCUMENTS = 200

DUMPFILE_NAME = os.path.join(GlobalConfiguration.project_root, "crawler/image_documents.pickle")

__author__ = 'daan'


def scrape_documents(n):
    """scrapes random wikipedia articles until it has at least n
    ImageDocuments and returns all the resulting ImageDocuments as a list"""
    result = []

    while len(result) < n:
        s = WikipediaScraper()
        result += s.get_documents()

    return result


def retrieve_saved_documents(dumpfilename=DUMPFILE_NAME):
    picklefile = open(dumpfilename, "rb")
    result = pickle.load(picklefile)
    picklefile.close()
    return result


def save_documents(documents, dumpfilename=DUMPFILE_NAME):
    picklefile = open(dumpfilename, "wb")
    pickle.dump(documents, picklefile)
    picklefile.close()


def main():
    documents = scrape_documents(MIN_DOCUMENTS)
    save_documents(documents)


if __name__ == '__main__':
    main()