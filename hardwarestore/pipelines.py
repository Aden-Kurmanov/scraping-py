from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient


class HardwarestorePipeline:

    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.db = client['geekBrains_data_from_net']

    def process_item(self, item, spider):
        db = self.db[spider.name]
        db.insert_one(item)
        return item


class HardwarestoreImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['image_links']:
            for img_url in item['image_links']:
                try:
                    yield scrapy.Request(img_url)
                    print()
                except Exception as e:
                    print("e: ", e)

    def item_completed(self, results, item, info):
        item['image_links'] = [it[1] for it in results if it[0]]
        return item
