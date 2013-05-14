#! /usr/bin/env python2.7
import logging

import os
import pickle
import GlobalConfiguration
from crawler.Scraper import WikipediaScraper
from tempfile import NamedTemporaryFile

import GlobalConfiguration
log = logging.getLogger(__name__)

DUMPFILE_NAME = os.path.join(GlobalConfiguration.project_root, "crawler/image_documents.pickle")

__author__ = 'daan'


def get_new_file():
    pickle_path = os.path.join(GlobalConfiguration.project_root, 'document_pickles')
    if not os.path.exists(pickle_path):
        os.makedirs(pickle_path)

    n = NamedTemporaryFile(
        prefix='imdoc_',
        dir=pickle_path,
        delete=False)

    return n


def scrape_documents():
    """scrapes random wikipedia articles into files until you hit Ctrl-C"""
    result = []

    doc_count = 0

    while True:
        s = WikipediaScraper()
        for doc in s.get_documents():
            temp_file = get_new_file()
            pickle.dump(doc, temp_file)
            temp_file.close()
            doc_count += 1
            if doc_count % 100 == 0:
                log.info('%d images and counting...')

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
    documents = scrape_documents()
    save_documents(documents)


if __name__ == '__main__':
    main()