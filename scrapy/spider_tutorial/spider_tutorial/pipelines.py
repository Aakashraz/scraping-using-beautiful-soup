# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
import logging
import os
from dotenv import load_dotenv
import sys
import site


load_dotenv(override=True)
mongo_uri = os.getenv("MONGODB_URI")

# print("python executable:", sys.executable)
# print(f"sys.path: {sys.path}")
# print(site.getsitepackages())


class MongodbPipeline:
    collection_name = 'full_transcript'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client['My_Database']
        logging.info("Spider opened: connected to MongoDB")
        # logging.warning('Spider Opened - Pipeline')

    def close_spider(self, spider):
        # logging.warning('Spider Closed - Pipeline')
        self.client.close()
        logging.info("Spider closed: MongoDB connection closed")

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(item)
        return item
