import scrapy
from scrapy.loader import Itemloader
from ..items import FilesToScrapeItem


class ImageToScrapeSpider(scrapy.Spider):
    name = 'downloader'
    start_urls = ['https://books.toscrape.com']

    def parse(self, response):
        articles = response.xpath('//article[@class="product_pod"]')
        for article in articles:
            loader = Itemloader(item=FilesToScrapeItem(), selector=article)
            relative_url = article.xpath('.//div[@class="image_container"]/a/img/@src').get()
            absolute_url = response.urljoin(relative_url)
            loader.add_value('image_urls', absolute_url)
            loader.add_xpath('book_name', './/h3/a/@title')
            yield loader.load_item()