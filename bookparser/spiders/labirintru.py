import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/']
    base_url = "https://www.labirint.ru"

    def parse(self, response: HtmlResponse):
        urls = response.xpath("//a[@class='product-title-link']/@href").getall()

        next_url = response.xpath("//a[@class='pagination-next__text']/@href").get()
        if next_url:
            yield response.follow(next_url, callback=self.parse)

        for url in urls:
            full_url = self.base_url + url
            yield response.follow(full_url, callback=self.book_parse)


    def book_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        price_old = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        price_new = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        publisher_name = response.xpath("//a[@data-event-label='publisher']/text()").get()
        publisher_url = self.base_url + response.xpath("//a[@data-event-label='publisher']/@href").get()
        rate = response.xpath("//div[@id='rate']/text()").get()
        about = response.xpath("//div[@id='product-about']/p/text()").get()
        url = response.url
        item = BookparserItem(url=url, name=name, price_old=price_old, price_new=price_new, publisher_name=publisher_name, publisher_url=publisher_url, rate=rate, about=about)
        yield item

