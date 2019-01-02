import scrapy
from pymongo import MongoClient
from datetime import datetime

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class PressballSpider(scrapy.spiders.CrawlSpider):
    name = 'pressball'
    # start_urls = ['https://www.pressball.by']
    start_urls = ['https://www.pressball.by/events']
    allowed_domains = ['pressball.by']
    server = MongoClient('mongodb://localhost:27017/')

    rules = (
        Rule(LinkExtractor(allow=(),
                           deny=(
                               r'pressball\.by\/events',
                               r'forum.pressball\.by\/posting\.php',
                               r'pressball\.by\/index.php',
                               r'pressball\.by\/voting\/vote.(pl|php)',
                               r'pressball\.by\/search\.php'
                           )),
             callback='save_link_meta', follow=True),
        Rule(LinkExtractor(allow=(r'pressball\.by\/news', ),
                           deny=(
                               r'\?page=\d+'
                           )),
             callback='save_link_meta', follow=True)
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
