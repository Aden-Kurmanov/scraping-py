import scrapy
from itemloaders.processors import MapCompose, TakeFirst
# from lxml import html


def price_to_int(prices):
    try:
        prices = int(prices.replace('\xa0', '').replace(" ", ""))
    except Exception:
        return prices
    return prices

# TODO  Пытался таким образом получить значения
# def get_properties(properties_block):
#     # content = html.fromstring(properties_block)
#     # tree = content.getroottree()
#     # print("tree: ", tree)
#     properties = {}
#     for it in properties_block:
#         tree = html.fromstring(it)
#         key = tree.xpath(".//dt[@class='def-list__term']/text()")
#         # key = it.xpath(".//dt[@class='def-list__term']/text()").get()
#         value = tree.xpath(".//dd[@class='def-list__definition']/text()")
#         # value = it.xpath(".//dd[@class='def-list__definition']/text()").get()
#         properties[key] = value
#         # properties[key] = " ".join(value.split())
#     return properties


class HardwarestoreItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_precessor=MapCompose(price_to_int), output_processor=TakeFirst())
    # price = scrapy.Field(input_precessor=MapCompose(lambda x: price_to_int(x)), output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    # properties = scrapy.Field(input_precessor=Compose(get_properties))
    # properties = scrapy.Field(input_precessor=MapCompose(get_properties))
    # properties = scrapy.Field(input_precessor=MapCompose(get_properties), output_processor=TakeFirst())
    properties = scrapy.Field(output_processor=TakeFirst())
    image_links = scrapy.Field()
