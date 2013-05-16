#! /usr/bin/env python2.7

import glob
import logging
import os
import pickle
import GlobalConfiguration
from crawler.Crawler import Crawler
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


def scrape_documents(
        min_count=0,
        url_seeds=GlobalConfiguration.DEFAULT_URL_SEEDS):

    doc_count = 0

    s = Crawler(url_seeds)
    docs = s.crawl(min_count)

    while min_count <= 0 or doc_count < min_count:
        for doc in docs:
            temp_file = get_new_file()
            pickle.dump(doc, temp_file)
            temp_file.close()
            log.debug('saved image doc from %s', doc.url)
            doc_count += 1
            if doc_count % 100 == 0:
                log.info('%d images and counting...', doc_count)

    log.info('finished indexing images.')
    log.info('%d documents indexed', doc_count)


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
    scrape_documents(
        min_count=100,
        url_seeds=GlobalConfiguration.DEFAULT_URL_SEEDS)


if __name__ == '__main__':
    main()