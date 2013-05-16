#! /usr/bin/env python2.7
import glob
import logging

import os
import pickle
import GlobalConfiguration
from crawler.Scraper import WikipediaScraper
from tempfile import NamedTemporaryFile

import GlobalConfiguration

PICKLE_PREFIX = 'imdoc_'
log = logging.getLogger(__name__)

PICKLE_PATH = os.path.join(GlobalConfiguration.project_root, 'document_pickles')

__author__ = 'daan'


def get_new_file():
    if not os.path.exists(PICKLE_PATH):
        os.makedirs(PICKLE_PATH)

    n = NamedTemporaryFile(
        prefix=PICKLE_PREFIX,
        dir=PICKLE_PATH,
        delete=False)

    return n


def scrape_documents(min_count=0):
    """scrapes random wikipedia articles into files until you hit Ctrl-C"""
    result = []

    doc_count = 0

    while True and (min_count == 0 or doc_count < min_count):
        s = WikipediaScraper()
        for doc in s.get_documents():
            temp_file = get_new_file()
            pickle.dump(doc, temp_file)
            temp_file.close()
            doc_count += 1
            if doc_count % 100 == 0:
                log.info('%d images and counting...', doc_count)

    return result


def retrieve_saved_documents():
    file_list = glob.glob(os.path.join(PICKLE_PATH, PICKLE_PREFIX + '*'))
    for dumpfilename in file_list:
        try:
            picklefile = open(dumpfilename, "rb")
            result = pickle.load(picklefile)
            picklefile.close()
            yield result
        except:
            # ignore any error since a single document is not that important
            log.info('Error uploading %s.', dumpfilename)
            pass


def main():
    scrape_documents(100)


if __name__ == '__main__':
    main()