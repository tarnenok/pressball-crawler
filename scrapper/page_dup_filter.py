from scrapper.settings import crawling_db


class PageDupFilter:
    def __init__(self, page_type_recognizer):
        self._page_type_recognizer = page_type_recognizer

        self._seen_article_urls = self._load_seen_urls()
        self._seen_urls_in_session = set()

    def update_filter(self, url):
        self._seen_urls_in_session.add(url)

        if url not in self._seen_article_urls\
                and self._page_type_recognizer.is_article(url):
            # TODO can improve performance by flushing data into DB not every time
            crawling_db['pressball_article_urls'].insert_one({'url': url})
            self._seen_article_urls.add(url)

    def url_seen_in_session(self, url):
        return url in self._seen_urls_in_session

    def url_seen(self, url):
        return url in self._seen_article_urls or url in self._seen_urls_in_session

    @staticmethod
    def _load_seen_urls():
        return set([item['url'] for item in crawling_db['pressball_article_urls'].find({}, {'_id': 0})])
