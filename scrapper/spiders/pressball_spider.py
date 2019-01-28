from datetime import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor

from scrapper.page_type_recognizer import PageTypeRecognizer
from scrapper.page_rank import PageRankBuilder
from scrapper.page_dup_filter import PageDupFilter
from scrapper.settings import crawling_db


class PressballSpider(scrapy.spiders.CrawlSpider):
    name = 'pressball'
    start_urls = ['https://www.pressball.by',
                  'https://www.pressball.by/news',
                  'https://www.pressball.by/pbonline',
                  'https://www.pressball.by/articles']

    allowed_domains = ['pressball.by']

    _ARTICLE_PATTERN_LIST = [
        r'pressball\.by\/news\/\w+\/\d+\/?$',
        r'pressball\.by\/articles\/\w+\/\w+\/\d+\/?$',
        r'pressball\.by\/pbonline\/\w+\/\d+\/?$']
    _OTHER_PAGES_PATTERN_LIST = [
        'pressball\.by\/news\/?\?page=\d+$',
        r'pressball\.by\/articles\/?\?p=\d+$',
        r'pressball\.by\/pbonline\/?\?p=\d+$'
    ]

    def __init__(self, *a, **kw):
        super(PressballSpider, self).__init__(*a, **kw)

        self._link_extractor = LinkExtractor(allow=tuple(self._ARTICLE_PATTERN_LIST + self._OTHER_PAGES_PATTERN_LIST), deny=())
        self._page_type_recognizer = PageTypeRecognizer(self._ARTICLE_PATTERN_LIST)
        self._page_dup_filter = PageDupFilter(self._page_type_recognizer)
        self._page_rank_builder = PageRankBuilder(self._page_type_recognizer,
                                                  self._link_extractor,
                                                  self._page_dup_filter)

    def parse(self, response):
        self._save_meta(response)
        response.meta['page_type'] = self._page_type_recognizer.recognize(response.url)

        urls = [link.url for link in self._link_extractor.extract_links(response)]
        new_urls = [link for link in urls if not self._page_dup_filter.url_seen_in_session(link)]

        page_rank, history_rank = self._page_rank_builder.build_combined_page_rank(response)
        if page_rank > 0:
            for link in new_urls:
                self._page_dup_filter.update_filter(link)
                yield scrapy.Request(link, meta={'history_rank': history_rank})

    def _save_meta(self, response):
        referer = response.request.headers.get('Referer', None)
        referer_str = referer.decode() if referer is not None else None

        crawling_db['pressball_crawl_stat'].insert_one({
            'url': response.url,
            'latency': response.meta['download_latency'],
            'links': [link.url for link in self._link_extractor.extract_links(response)],
            'time': datetime.now(),
            'referer': referer_str
        })
