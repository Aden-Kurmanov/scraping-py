import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def price_to_int(price):
    try:
        return int(price.replace("\xa0", "").replace(" ", ""))
    except Exception as _:
        return price


def get_image_links(properties_block):
    properties = {}
    for it in properties_block:
        key = it.xpath(".//dt[@class='def-list__term']/text()").get()
        value = it.xpath(".//dd[@class='def-list__definition']/text()").get()
        properties[key] = " ".join(value.split())
    return properties


class HardwarestoreItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_precessor=MapCompose(price_to_int), output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    properties = scrapy.Field(input_precessor=MapCompose(get_image_links), output_processor=TakeFirst())
    image_links = scrapy.Field()
