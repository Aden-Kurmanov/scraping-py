import scrapy
from scrapy.http import HtmlResponse
import re
import json
from scrapy.loader import ItemLoader
from instagramparser.items import InstagramparserItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com']
    insta_login_url = 'https://www.instagram.com/accounts/login/ajax/'
    insta_login = ''
    insta_password = ''
    parse_accounts = ['englishwords_free', 'my_english_affair']
    hash = "8c2a529969ee035a5063f2fc8602a0fd"

    url_sub = 'https://i.instagram.com/api/v1/friendships/'
    list_subscriptions = [{'url': f"{url_sub}", 'is_follower': False}, {'url': f"{url_sub}", 'is_follower': True}]

    def parse(self, response: HtmlResponse):
        csrf_token = self.get_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.insta_login_url,
            method='POST',
            callback=self.login,
            formdata={
                'username': self.insta_login,
                'enc_password': self.insta_password
            },
            headers={'X-CSRFToken': csrf_token}
        )

    def login(self, response: HtmlResponse):
        data = response.json()
        if data['authenticated']:
            for account in self.parse_accounts:
                yield response.follow(
                    f"/{account}",
                    callback=self.account,
                    cb_kwargs={'account': account}
                )

    def account(self, response: HtmlResponse, account: str):
        account_id = self.get_account_id(response.text, account)
        for sub in self.list_subscriptions:
            url = f"{sub['url']}{account_id}/{'followers' if sub['is_follower'] else 'following'}/?count=12"
            yield response.follow(
                url=url,
                callback=self.account_subscriptions,
                cb_kwargs={
                    'account': account,
                    'account_id': account_id,
                    'url': url,
                    'is_follower': sub['is_follower']
                }
            )

    def account_subscriptions(self, response: HtmlResponse, account: str, account_id: int, url: str, is_follower: bool):
        data = response.json()

        if data.get('next_max_id') is not None:
            yield response.follow(
                url=f"{url}&max_id={data.get('next_max_id')}",
                callback=self.account_subscriptions,
                cb_kwargs={
                    'account': account,
                    'account_id': account_id,
                    'url': url,
                    'is_follower': is_follower
                }
            )

        for user in data.get('users'):
            username = user.get('username')
            url_account = f"{self.start_urls[0]}/{username}"
            avatar_url = user.get('profile_pic_url')
            yield response.follow(
                url=url_account,
                callback=self.prepare_account,
                cb_kwargs={
                    'account': username,
                    'avatar_url': avatar_url,
                    'is_follower': is_follower,
                    'main_id': account_id,
                    'main_account': account
                }
            )

    def prepare_account(
            self,
            response: HtmlResponse,
            account: str,
            avatar_url: str,
            is_follower: bool,
            main_id: int,
            main_account: str
    ):
        account_id = self.get_account_id(response.text, account)
        loader = ItemLoader(item=InstagramparserItem(), response=response)
        loader.add_value('main_id', main_id)
        loader.add_value('main_account', main_account)
        loader.add_value('is_sub_follower', is_follower)
        loader.add_value('sub_name', account)
        loader.add_value('sub_id', account_id)
        loader.add_value('sub_avatar_info', avatar_url)
        yield loader.load_item()

    def get_csrf_token(self, text: str):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(":").pop().replace(r'"', '')

    def get_account_id(self, text: str, account: str):
        grouped = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % account, text).group()
        return json.loads(grouped).get('id')
