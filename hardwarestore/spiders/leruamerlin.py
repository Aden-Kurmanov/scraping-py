import scrapy
from scrapy.http import HtmlResponse
from hardwarestore.items import HardwarestoreItem
from scrapy.loader import ItemLoader


class LeruamerlinSpider(scrapy.Spider):
    name = 'leruamerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://leroymerlin.ru/search/?q={query}"]

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-qa-product-name]")

        next_url = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()
        if next_url:
            yield response.follow(next_url, callback=self.parse)

        for link in links:
            yield response.follow(link, callback=self.parse_link)

    def parse_link(self, response: HtmlResponse):
        loader = ItemLoader(item=HardwarestoreItem(), response=response)
        loader.add_xpath("name", "//h1[@slot='title']/text()")
        loader.add_xpath("price", "//span[@slot='price']/text()")
        loader.add_value("link", response.url)
        # loader.add_xpath("properties", "//div[@class='def-list__group']")
        loader.add_xpath("image_links", "//img[@itemprop='image' and @alt='product image']/@src")

        properties_blocks = response.xpath("//div[@class='def-list__group']")
        properties = {}
        for it in properties_blocks:
            key = it.xpath(".//dt[@class='def-list__term']/text()").get()
            value = it.xpath(".//dd[@class='def-list__definition']/text()").get()
            properties[key] = " ".join(value.split())
        loader.add_value("properties", properties)
        yield loader.load_item()
