from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['geekBrains_data_from_net']['instagram']


def get_users(account: str, is_followers: bool):
    return db.find({'$and': [{'main_account': account}, {'is_sub_follower': is_followers}]})


data = []
for item in get_users('', False):
    data.append(item)
print(len(data))
