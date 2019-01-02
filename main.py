from scrapy import cmdline
from scrapy.linkextractors import LinkExtractor

if __name__ == '__main__':
    cmdline.execute("scrapy crawl pressball".split())