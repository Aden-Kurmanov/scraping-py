from lxml import html
import requests
from pprint import pprint as p
from pymongo import MongoClient

client = MongoClient("127.0.0.1", 27017)
db = client['geekBrains_data_from_net']
news = db.news

url = 'https://lenta.ru/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

response = requests.get(url, headers=headers)

dom = html.fromstring(response.text)

top_section = dom.xpath("//section[contains(@class, 'js-top-seven')]")[0]
top_main_news = top_section[0].xpath(".//div[@class='first-item']")[0]
top_news = top_section.xpath(".//div[@class='item']")

top_main_news_data = {
    'source': 'https://lenta.ru/',
    'name': top_main_news.xpath(".//h2/a/text()")[0].replace('\xa0', ' '),
    'link': url + top_main_news.xpath(".//a[contains(@class, 'topic-title-pic__link')]/@href")[0],
    'date': top_main_news.xpath(".//time[@datetime]/@datetime")[0]
}

is_exist = False
for _ in news.find({'link': top_main_news_data['link']}):
    is_exist = True
    break
if not is_exist:
    news.insert_one(top_main_news_data)

for item in top_news:
    item_info = {
        'source': 'https://lenta.ru/',
        'name': item.xpath("./a/text()")[0].replace('\xa0', ' '),
        'link': url + item.xpath("./a[@href]/@href")[0],
        'date': item.xpath(".//time[@datetime]/@datetime")[0]
    }

    is_exist = False
    for _ in news.find({'link': item_info['link']}):
        is_exist = True
        break

    if not is_exist:
        news.insert_one(item_info)

for item in news.find({}):
    p(item)
