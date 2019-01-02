BOT_NAME = 'scrapper'

SPIDER_MODULES = ['scrapper.spiders']
NEWSPIDER_MODULE = 'scrapper.spiders'

DUPEFILTER_CLASS = 'scrapy.dupefilters.RFPDupeFilter'

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 0
DOWNLOAD_TIMEOUT = 60

AUTOTHROTTLE_ENABLED = False

COOKIES_ENABLED = False
ROBOTSTXT_OBEY = False

# Breadth first observation
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'
