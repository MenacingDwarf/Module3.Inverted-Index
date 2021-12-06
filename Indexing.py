from lemmatization import clear_text
from collections import Counter
from html_parser import get_text_url, info_extract
import pymongo
from elias import Elias_Gamma
from bitarray import bitarray
from bson.binary import Binary

class Indexing:
    def __init__(self):
        self.urls_ids = {}
        self.indexing_words = {}

    def clear_index(self):
        self.urls_ids = {}
        self.indexing_words = {}

    # Get url id from list of urls or new
    def get_url_id(self, url):
        if not self.urls_ids:
            new_id = 0
        else:
            max_id = max(self.urls_ids.keys())
            new_id = max_id + 1
        self.urls_ids[new_id] = url
        return new_id

    # Get top 50 lematized words from url
    def get_url_words(self, url):
        text = info_extract(get_text_url(url))
        c = Counter(clear_text(text))
        return [word[0] for word in c.most_common(50)]


    # Add word to index (just dict or MongoDB)
    def add_word(self, word, url_id):
        if word in self.indexing_words:
            self.indexing_words[word].append(url_id)
        else:
            self.indexing_words[word] = [url_id]

    # Return list of urls from report file
    def parse_report(self, report_path):
        with open(report_path, 'r') as input_file:
            text = input_file.read()
        list_of_rows = text.split('\n')
        list_status_url = []
        for row in list_of_rows:
            list_status_url.append(row.strip().split('    '))
        url_list = []
        for status_url in list_status_url:
            if status_url[0] == 'OK':
                url_list.append(status_url[1])
        return url_list

    # Get all words from url and add them to index
    def parse_url(self, url):
        words = self.get_url_words(url)
        url_id = self.get_url_id(url)
        for word in words:
            self.add_word(word, url_id)

    # Parse all urls from report file and add to index
    def add_to_index(self, report_path):
        report_urls = self.parse_report(report_path)
        for url in report_urls[:10]:  # Пока только 10 :)
            self.parse_url(url)

    # Return list of URLs that contain specified word
    def find_by_word(self, word):
        urls = []
        clear_word = clear_text(word)[0]
        if clear_word in self.indexing_words:
            for index in self.indexing_words[clear_word]:
                urls.append(self.urls_ids[index])
        return urls

if __name__ == '__main__':
    indexing = Indexing()
    indexing.clear_index()
    indexing.add_to_index('reports/slurp.report')
    #print(indexing.urls_ids)
    #print(indexing.indexing_words)
    print(indexing.find_by_word("рамен"))
