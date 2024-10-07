import scrapy


class AdamchoiSpider(scrapy.Spider):
    name = "adamchoi"
    allowed_domains = ["adamchoi.co.uk"]
    start_urls = ["https://adamchoi.co.uk"]

    def parse(self, response):
        pass
