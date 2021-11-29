import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import sys
import time
import hyperlink

class Indexing:
    def __init__(self):
        self.urls_ids = {}
        self.indexing_words = {}

    # Get url id from list of urls or new
    def get_url_id(self, url):
        if not self.urls_ids:
            new_id = 0
        else:
            max_id = max(self.urls_ids, key=self.urls_ids.get)
            new_id = max_id + 1

        self.urls_ids[new_id] = url
        return new_id

    # Get top 50 lematized words from url
    def get_url_words(self, url):
        pass

    # Add word to index (just dict or MongoDB)
    def add_world(self, word, url_id):
        pass

    # Return list of urls from report file
    def parse_report(self, report_file):
        pass

    # Get all words from url and add them to index
    def parse_url(self, url):
        words = self.get_url_words(url)
        url_id = self.get_url_id(url)
        for word in words:
            self.add_world(word, url_id)

    # Parse all urls from report file and add to index
    def add_to_index(self, report_file):
        report_urls = self.parse_report(report_file)
        for url in report_urls:
            self.parse_url(url)

if __name__ == '__main__':
    indexing = Indexing()
    indexing.add_to_index("reports/slurp.report")
