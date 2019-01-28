import re


class PageTypeRecognizer:
    ARTICLE_PAGE = 0
    OTHER_PAGE = 1

    def __init__(self, article_pattern_list):
        self.regex_list = [re.compile(pattern) for pattern in article_pattern_list]

    def recognize(self, url):
        for regex in self.regex_list:
            if regex.search(url) is not None:
                return self.ARTICLE_PAGE
        return self.OTHER_PAGE

    def is_article(self, url):
        return self.recognize(url) == self.ARTICLE_PAGE
