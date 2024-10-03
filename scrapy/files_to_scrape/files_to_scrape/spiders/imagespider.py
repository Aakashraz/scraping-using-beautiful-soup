import scrapy
from scrapy.loader import ItemLoader
from ..items import ImagesToScrapeItem


class ImageToScrapeSpider(scrapy.Spider):
    name = 'downloader'
    start_urls = ['https://books.toscrape.com']

    def parse(self, response):
        articles = response.xpath('//article[@class="product_pod"]')
        for article in articles:
            loader = ItemLoader(item=ImagesToScrapeItem(), selector=article)
            relative_url = article.xpath('.//div[@class="image_container"]/a/img/@src').get()
            absolute_url = response.urljoin(relative_url)
            loader.add_value('image_urls', absolute_url)
            loader.add_xpath('book_name', './/h3/a/@title')
            # the @ symbol in XPath refers to an attribute of an HTML element
            yield loader.load_item()

# use for Images Pipeline,
# ITEM_PIPELINES = {"scrapy.pipelines.images.ImagesPipeline": 1}


