import scrapy
from itemloaders.processors import TakeFirst


class InstagramparserItem(scrapy.Item):
    main_id = scrapy.Field(output_processor=TakeFirst())
    main_account = scrapy.Field(output_processor=TakeFirst())
    is_sub_follower = scrapy.Field(output_processor=TakeFirst())
    sub_name = scrapy.Field(output_processor=TakeFirst())
    sub_id = scrapy.Field(output_processor=TakeFirst())
    sub_avatar_info = scrapy.Field(output_processor=TakeFirst())
