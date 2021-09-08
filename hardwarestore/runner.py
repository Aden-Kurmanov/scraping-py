from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from hardwarestore import settings
from hardwarestore.spiders.leruamerlin import LeruamerlinSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    search = input("Что вы ищите?: ")
    process = CrawlerProcess(crawler_settings)
    process.crawl(LeruamerlinSpider, query=search)
    process.start()

