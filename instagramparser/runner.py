from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from pymongo import MongoClient

from instagramparser import settings
from instagramparser.spiders.instagram import InstagramSpider

if __name__ == '__main__':
    client = MongoClient('127.0.0.1', 27017)
    db = client['geekBrains_data_from_net']['instagram']
    db.delete_many({})
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstagramSpider)
    process.start()
