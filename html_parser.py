from bs4 import BeautifulSoup, Tag
import requests
from user_agent import generate_user_agent


def get_text_url(url):
    headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
    ritem = requests.get(url, headers=headers)
    return ritem.text


def info_extract(text):
    isoup = BeautifulSoup(text, features='html.parser')
    tlist = []
    def info_extract_helper(inlist, count = 0):
        if(isinstance(inlist, list)):
            for q in inlist:
                if(isinstance(q, Tag)):
                    if not (str(q).startswith('<script') or str(q).startswith('<style')):
                        info_extract_helper(q.contents, count + 1)
                else:
                    extracted_str = q.strip()
                    if(extracted_str and (count > 1)):
                        tlist.append(extracted_str)
    info_extract_helper([isoup])
    return ' '.join(tlist)


def get_url(path):
    with open(path, 'r') as input_file:
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


if __name__ == '__main__':
    res = get_url('spbu_report.txt')
    print(res[:5])
