from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class InstagramparserPipeline:

    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.db = client['geekBrains_data_from_net']['instagram']

    def process_item(self, item, spider):
        self.db.insert_one(dict(item))
        return item


class InstagramparserImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['sub_avatar_info']:
            try:
                yield scrapy.Request(item['sub_avatar_info'])
            except Exception as e:
                print("Images Error: ", e)

    def item_completed(self, results, item, info):
        item['sub_avatar_info'] = results[0][1] if results[0] else None
        return item
