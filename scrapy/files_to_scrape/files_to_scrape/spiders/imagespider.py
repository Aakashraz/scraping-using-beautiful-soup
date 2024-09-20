import scrapy
from scrapy.loader import Itemloader
from ..items import FilesToScrapeItem


class ImageToScrapeSpider(scrapy.Spider):
    name = 'downloader'
    start_urls = ['https://books.toscrape.com']

    def parse(self, response):
        pass