import pickle
from Scraper import WikipediaScraper

__author__ = 'daan'


def scrape_documents(n):
    """scrapes random wikipedia articles until it has at least n
    ImageDocuments and returns all the resulting ImageDocuments as a list"""
    result = []

    while len(result) < n:
        s = WikipediaScraper()
        result += s.get_documents()

    return result


def retrieve_saved_documents():
    return pickle.load(open("image_documents.pickle", "rb"))


def main():
    documents = scrape_documents(200)

    pickle.dump(documents, open("image_documents.pickle", "wb"))


if __name__ == '__main__':
    main()