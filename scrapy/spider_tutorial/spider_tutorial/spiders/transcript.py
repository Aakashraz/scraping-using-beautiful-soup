import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptSpider(CrawlSpider):
    name = "transcript"
    allowed_domains = ["subslikescript.com"]
    start_urls = ["https://subslikescript.com"]

    # Key Concepts:
    #
    #     LinkExtractor: Identifies which links to follow based on patterns (allow and deny).
    #     callback: Specifies the method to call when certain links are followed (e.g., parse_item).
    #     Rules: Define how the spider behaves when encountering links on the page (whether to follow or extract data).
    rules = (Rule(LinkExtractor(allow=r"Items/"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        item = {}
        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
        return item
