import collections


class PageRankBuilder:
    PAGE_RANK_HISTORY_LENGTH = 3

    def __init__(self, page_type_recognizer, link_extractor, page_dup_filter):
        self.page_type_recognizer = page_type_recognizer
        self.link_extractor = link_extractor
        self.page_duplicator = page_dup_filter

    def build_page_rank(self, response):
        urls = [link.url for link in self.link_extractor.extract_links(response)]
        new_urls = [url for url in urls if not self.page_duplicator.url_seen(url)]
        new_article_urls = [url for url in new_urls if self.page_type_recognizer.is_article(url)]

        return len(new_article_urls)

    def build_combined_page_rank(self, response):
        page_rank = self.build_page_rank(response)
        if 'history_rank' not in response.request.meta.keys():
            history_rank = collections.deque(maxlen=self.PAGE_RANK_HISTORY_LENGTH)
        else:
            history_rank = response.request.meta['history_rank'].copy()

        history_rank.append(page_rank)
        return sum(history_rank), history_rank
