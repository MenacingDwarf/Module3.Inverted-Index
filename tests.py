import unittest
from Indexing import Indexing

class BaseCrawlerTestCase(unittest.TestCase):
    report_files = ""
    words = {}

    @classmethod
    def setUpClass(cls):
        print(f'\n\nRunning Test Case: {cls.__name__}...')
        cls.indexing = Indexing()
        for report in cls.report_files:
            cls.indexing.add_to_index(report)

    def testWord(self, word_index=0, skip=True):
        if skip:
            self.skipTest("Internal method")

        word = list(self.words.keys())[word_index]
        print(f'\n----Testing word: {word}...')
        self.assertListEqual(self.indexing.find_by_word(word), self.words[word])

    def testWord1(self):
        self.testWord(0, False)

    def testWord2(self):
        self.testWord(1, False)

    def testWord3(self):
        self.testWord(2, False)

class TestSlurpWebsite(BaseCrawlerTestCase):
    report_files = ["reports/slurp.report"]
    words = {
        'лапша': ['https://ramenslurp.ru/', 'https://ramenslurp.ru/menu'],
        'сервис': ['https://ramenslurp.ru/contacts', 'https://ramenslurp.ru/delivery'],
        'блюдо': ['https://ramenslurp.ru/', 'https://ramenslurp.ru/delivery']
    }

class TestBurgers(BaseCrawlerTestCase):
    report_files = ["reports/bureau.report", "reports/citygrills.report"]
    words = {
        'бургер': ['https://barbureau.ru/', 'https://barbureau.ru/photochki', 'https://barbureau.ru/menu_photo', 'https://citygrillexpress.ru/'],
        'франшиза': ['https://citygrillexpress.ru/', 'https://citygrillexpress.ru/contacts', 'https://citygrillexpress.ru/payment', 'https://citygrillexpress.ru/agreements'],
        'блюдо': []
    }

def get_list_of_tests():
    return list(BaseCrawlerTestCase.__subclasses__())

def run_all_tests():
    loader = unittest.TestLoader()
    cases = []
    for cls in get_list_of_tests():
        cases.append(loader.loadTestsFromTestCase(cls))
    suite = unittest.TestSuite(cases)
    runner = unittest.TextTestRunner()
    runner.run(suite)


def run_single_test(test_case):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite([loader.loadTestsFromTestCase(test_case)])
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    run_all_tests()
