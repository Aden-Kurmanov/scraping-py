from pymongo import MongoClient


class BookparserPipeline:

    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.db = client['geekBrains_data_from_net']

    def process_item(self, item, spider):
        item['price_old'] = int(item['price_old'])
        item['price_new'] = int(item['price_new'])
        item['rate'] = float(item['rate'])
        db = self.db[spider.name]
        db.insert_one(item)
        return item
