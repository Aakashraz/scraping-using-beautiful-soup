# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class FilesToScrapeItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    book_name = scrapy.Field(
        output_processor=TakeFirst()
    )

