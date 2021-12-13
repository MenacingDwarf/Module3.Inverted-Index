import requests
import sys
from pathlib import Path
import json

class HtmlCollector():
    def __init__(self, report_path, index=1):
        self.index = index
        self.urls_list = self.parse_report(report_path)
        self.htmls_subfolder = Path(report_path).stem
        Path(f'htmls/{self.htmls_subfolder}').mkdir(parents=True, exist_ok=True)

    def save_html(self, url):
        r = requests.get(url)
        result = {'url': url, 'html': r.text}
        with open(f'htmls/{self.htmls_subfolder}/page{self.index}.json', "a") as file:
            file.write(json.dumps(result))
        self.index += 1

    def is_document(self, url):
        lower_url = url.lower()
        return lower_url.endswith('.doc') or lower_url.endswith('.docx') or lower_url.endswith('.pdf')

    def is_image(self, url):
        lower_url = url.lower()
        return lower_url.endswith('.jpg') or lower_url.endswith('.jpeg') or lower_url.endswith('.gif') or lower_url.endswith('.svg')

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

    def run(self, first_index=None, last_index=None):
        print(f'Start parsing {self.htmls_subfolder}...')
        url_count = 0

        urls = self.urls_list[40000 : 80000]

        for url in urls:
            try:
                if not self.is_document(url) and not self.is_image(url):
                    self.save_html(url)
            except Exception as e:
                print(f'-- Collection of {url} raise error: {e.data}')
            finally:
                url_count += 1
                print(f'-- Parsed URLs: {url_count} of {len(urls)}...')

if __name__ == '__main__':
    collector = HtmlCollector(str(sys.argv[1]), index=21614)
    collector.run(first_index=22528, last_index=40000)
