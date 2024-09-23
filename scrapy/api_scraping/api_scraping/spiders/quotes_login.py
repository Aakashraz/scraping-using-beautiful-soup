import scrapy
from scrapy import FormRequest


class QuotesLoginSpider(scrapy.Spider):
    name = "quotes_login"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/login"]

    def parse(self, response):
        csrf_token = response.xpath('//input[@name="csrf_token"]/@value').get()
        yield FormRequest.from_response(
            response,
            formxpath='//form',  #this is the xpath to select the whole form
            formdata={
                'csrf_token': csrf_token,
                'username': 'admin',
                'password': 'admin'
            },
            callback=self.after_login,
            # to pass to the another method
            meta={'csrf': csrf_token}
        )

    def after_login(self, response):
        logout_xpath = response.xpath('//a[@href="/logout"]/text()').get()
        if logout_xpath == 'Logout':
            print("Successfully Logged in~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(f"CSRF: {response.meta['csrf']}")
