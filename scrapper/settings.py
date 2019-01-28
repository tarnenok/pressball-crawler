from pymongo import MongoClient

BOT_NAME = 'scrapper'

SPIDER_MODULES = ['scrapper.spiders']
NEWSPIDER_MODULE = 'scrapper.spiders'

DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 0
DOWNLOAD_TIMEOUT = 60

AUTOTHROTTLE_ENABLED = False

COOKIES_ENABLED = False
ROBOTSTXT_OBEY = False

mongo_server = MongoClient('mongodb://127.0.0.1:27020/')
crawling_db = mongo_server['crawling']
