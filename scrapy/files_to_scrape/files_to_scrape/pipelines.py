# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
# from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request
# from scrapy.http.request import NO_CALLBACK


class BooksToScrapePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        urls = item.get(self.images_urls_field, [])
        return [Request(u) for u in urls]