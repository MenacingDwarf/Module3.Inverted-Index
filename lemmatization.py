"""Import required libraries"""
import re
import string
from nltk.corpus import stopwords
import pymorphy2
from html_parser import get_url, get_text_url, info_extract
from collections import Counter
morph = pymorphy2.MorphAnalyzer()
stop_words = stopwords.words("russian")


"""Text clearing function"""
def clear_text(x):
    r = re.compile("[а-яА-Я]+")
    x = x.lower()  # Lowercase the text
    x = re.sub('[%s]' % re.escape(string.punctuation), ' ', x)  # Remove punctuations
    x = re.sub(r'\w*\d+\w*', '', x)  # Remove numbers
    x = re.sub(r'\s{2,}', ' ', x)  # Replace the over spaces
    x = [word for word in filter(r.match, x.split())]  # Russian symbols
    x = [word for word in x if len(word) > 4]  # Remove short words
    x = [morph.normal_forms(word)[0] for word in x]  # Normalization words
    x = [word for word in x if word not in stop_words]  # Remove stop words
    return x


if __name__ == '__main__':
    res = get_url('spbu_report.txt')
    c = Counter(clear_text(info_extract(get_txt_url(res[0]))))
    print([word[0] for word in c.most_common(50)])