import scrapy
from scrapy.http import HtmlResponse

# TODO Еще в работе
class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com']
    insta_login_url = 'https://www.instagram.com/accounts/login/ajax/'
    insta_login = ''
    insta_password = ''

    def parse(self, response: HtmlResponse):
        yield scrapy.FormRequest(
            self.insta_login_url,
            method='POST',
            callback=self.login,
            formdata={
                'username': self.insta_login,
                'enc_password': self.insta_password
            }
        )

    def login(self, response: HtmlResponse):
        pass
