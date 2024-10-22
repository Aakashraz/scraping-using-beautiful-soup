import scrapy
from scrapy_splash import SplashRequest


class BeerSpider(scrapy.Spider):
    name = 'beer'

    def start_requests(self):
        url = 'https://www.beerwulf.com/en-gb/c/mixedbeercases'
        yield SplashRequest(url, callback=self.parse)

    def parse(self, response):
        products = response.css('a.product.search-product.product-info-container.bw-plp-product-card.draught-product.notranslate')
        for product in products:
            yield{
                'name': product.css('div.product-name::text').get(),
                'price': product.css('span.price::text').get()
            }
