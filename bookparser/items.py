import scrapy

class BookparserItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    price_old = scrapy.Field()
    price_new = scrapy.Field()
    publisher_name = scrapy.Field()
    publisher_url = scrapy.Field()
    rate = scrapy.Field()
    about = scrapy.Field()
    _id = scrapy.Field()
