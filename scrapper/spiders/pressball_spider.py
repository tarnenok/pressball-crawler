import scrapy
from pymongo import MongoClient
from datetime import datetime


class PressballSpider(scrapy.Spider):
    name = 'pressball'
    start_urls = ['https://www.pressball.by']
    allowed_domains = ['www.pressball.by']
    server = MongoClient('mongodb://localhost:27017/')

    def parse(self, response):
        links = response.css('a::attr(href)').extract()

        self.server['crawling']['pressball_pages'].insert_one({
            'url': response.url,
            'latency': response.meta['download_latency'],
            'time': datetime.now(),
            'links': 'links'
        })

        for link in links:
            next_link = response.urljoin(link)
            yield scrapy.Request(next_link)
