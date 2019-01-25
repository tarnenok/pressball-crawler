import scrapy
from pymongo import MongoClient
from datetime import datetime

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class PressballSpider(scrapy.spiders.CrawlSpider):
    name = 'pressball'
    start_urls = ['https://www.pressball.by',
                  'https://www.pressball.by/news',
                  'https://www.pressball.by/pbonline',
                  'https://www.pressball.by/articles']

    allowed_domains = ['pressball.by']
    server = MongoClient('mongodb://127.0.0.1:27017/')

    rules = (
        Rule(LinkExtractor(allow=(r'pressball\.by\/news\/\w+\/\d+\/?',
                                  r'pressball\.by\/news\/?\?page=\d+',

                                  r'pressball\.by\/articles\/\w+\/\w+\/\d+\/?',
                                  r'pressball\.by\/articles\/?\?p=\d+',

                                  r'pressball\.by\/pbonline\/\w+\/\d+\/?',
                                  r'pressball\.by\/pbonline\/?\?p=\d+',),
                           deny=()),
             callback='save_link_meta', follow=True),
    )

    def save_link_meta(self, response):
        referer = response.request.headers.get('Referer', None)
        referer_str = referer.decode() if referer is not None else None

        self.server['crawling']['pressball_pages'].insert_one({
            'url': response.url,
            'latency': response.meta['download_latency'],
            'time': datetime.now(),
            'links': [link for link in response.css('a::attr(href)').extract() if self.allowed_domains[0] in link],
            'referer': referer_str
        })
