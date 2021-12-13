from lemmatization import clear_text
from collections import Counter
from html_parser import get_text_url, info_extract
from elias import Elias_Gamma
import psycopg2
import numpy as np

class Indexing_psql:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="ec2-176-34-105-15.eu-west-1.compute.amazonaws.com",
            database="d9sv3qqpfj9q97",
            user="qasfuuagthzqlv",
            password="c83a6d6e61cdd075f597f4c9b7fb09f1d2eef87867d49ab848b43d71bc2c89c7"
        )

    def clear_index(self):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM url;")
        cur.execute("DELETE FROM inv_ind;")
        cur.execute("DELETE FROM inv_ind_el;")
        self.conn.commit()

    def is_document(self, url):
        lower_url = url.lower()
        return lower_url.endswith('.doc') or lower_url.endswith('.docx') or lower_url.endswith('.pdf')

    def is_image(self, url):
        lower_url = url.lower()
        return lower_url.endswith('.jpg') or lower_url.endswith('.jpeg') or lower_url.endswith('.gif') or lower_url.endswith('.svg')


    def get_max_id(self):
        cur = self.conn.cursor()
        cur.execute("SELECT MAX(id) FROM url;")
        max_id = cur.fetchone()
        if max_id is None:
            return None
        return max_id[0]

    # Get url id from list of urls or new
    def get_url_id(self, url):
        max_id = self.get_max_id()
        if max_id is None:
            new_id = 2
        else:
            new_id = max_id + 1
        el_id = Elias_Gamma(new_id)
        cur = self.conn.cursor()
        cur.execute("INSERT INTO url VALUES (%s, %s, %s);", [new_id, el_id, url])
        self.conn.commit()
        return new_id, el_id

    # Get top 50 lematized words from url
    def get_url_words(self, url):
        text = info_extract(get_text_url(url))
        c = Counter(clear_text(text))
        return [word[0] for word in c.most_common(50)]

    def get_ind(self, word):
        cur = self.conn.cursor()
        cur.execute("SELECT postlist FROM inv_ind WHERE word = %s", [word])
        ind = cur.fetchone()
        cur.execute("SELECT postlist FROM inv_ind_el WHERE word = %s", [word])
        ind_el = cur.fetchone()
        if ind is None:
            return None, None
        return ind[0], ind_el[0]

    # Add word to index
    def add_word(self, word, url_id, el_id):
        cur = self.conn.cursor()
        ind_word, ind_el_word = self.get_ind(word)
        if ind_word is None:
            cur.execute("INSERT INTO inv_ind VALUES (%s, %s);", [word, [url_id]])
            cur.execute("INSERT INTO inv_ind_el VALUES (%s, %s);", [word, el_id])
        else:
            ind_word.append(url_id)
            new_el_id = ind_el_word + el_id
            cur.execute("UPDATE inv_ind SET postlist = %s WHERE word = %s;", [ind_word, word])
            cur.execute("UPDATE inv_ind_el SET postlist = %s WHERE word = %s;", [new_el_id, word])
        self.conn.commit()

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
        if not self.is_document(url) and not self.is_image(url):
            words = self.get_url_words(url)
            url_id, el_id = self.get_url_id(url)
            for word in words:
                self.add_word(word, url_id, el_id)

    # Parse all urls from report file and add to index
    def add_to_index(self, report_path):
        report_urls = self.parse_report(report_path)
        for url in report_urls[0:10]:  # Пока только 10 :)
            self.parse_url(url)

    # Return list of URLs that contain specified word
    def find_by_word(self, word):
        urls = []
        if len(word) <= 3:
            print("Word is to short")
            return urls
        clear_word = clear_text(word)[0]
        ind_word, ind_el_word = self.get_ind(clear_word)
        if ind_word is None:
            print("Word not in index")
            return urls
        else:
            cur = self.conn.cursor()
            cur.execute("SELECT url from url where id in (" + str(ind_word)[1:-1] + ")")
            urls = cur.fetchall()
        return set(np.ravel(urls))

    def find_query(self, query):
        word_arr = query.strip().split()
        res_set = set()
        for word in word_arr:
            add_set = self.find_by_word(word)
            if res_set:
                res_set = res_set.intersection(add_set)
            else:
                res_set = add_set
        return res_set


if __name__ == '__main__':
    indexing = Indexing_psql()
    #indexing.clear_index()
    print(indexing.find_query("ректор спбгу"))
    #ind_word, el_ind = indexing.get_ind('ректор')
    #print(bytes(el_ind))
    #print(ind_word)
