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
    # In Scrapy, when using CrawlSpider and Rule, you can specify callback methods using strings.
    # Scrapy will automatically handle finding and calling these methods on the spider instance,
    # which is why self isn't needed explicitly in your code snippet. However, when coding outside of such a context,
    # or if you want explicit control, you would use self.

    def parse_item(self, response):
        yield{
            'TITLE': response.css('.product_main h1::text').get(),
            'PRICE': response.css('.price_color::text').get(),
            # the below code to fetch availability should use the strip() to remove
            # '\n' character which is printed ambiguously
            'AVAILABILITY': response.css('.availability::text')[1].get().strip().replace('\n', ''),
        }