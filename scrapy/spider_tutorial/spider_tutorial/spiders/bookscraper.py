from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class BookSpider(CrawlSpider):
    name = "bookcrawler"
    allowed_domains = ['toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    rules = (
        Rule(LinkExtractor(allow="catalogue/category")),
        Rule(LinkExtractor(allow="catalogue", deny="category"), callback='parse_item'),
    )

    def parse_item(self, response):
        yield{
            'TITLE': response.css('.product_main h1::text').get(),
            'PRICE': response.css('.price_color::text').get(),
            # the below code to fetch availability should use the strip() to remove
            # '\n' character which is printed ambiguously
            'AVAILABILITY': response.css('.availability::text')[1].get().strip().replace('\n', ''),
        }