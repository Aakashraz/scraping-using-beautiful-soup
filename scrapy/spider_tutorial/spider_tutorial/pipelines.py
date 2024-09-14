# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
import sqlite3
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


class SQLitePipeline:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def open_spider(self, spider):
        try:
            self.connection = sqlite3.connect('transcripts.db')
            self.cursor = self.connection.cursor()
            # create table if not exists
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS transcripts(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    plot TEXT,
                    full_script TEXT,
                    url TEXT
                )
            ''')
            self.connection.commit()
            logging.info("SQLite Pipeline opened: connected to SQLite")
        except sqlite3.Error as e:
            logging.error(f"Error while creating table: {e}")
            raise
    # the benefits of using 'raise' approach:
    # You get to log the error (for debugging purposes).
    # The program doesn't continue running with a broken database connection.
    # Any error handling mechanism at a higher level (e.g., Scrapy's error handling) can catch
    # and deal with this exception.

    def close_spider(self, spider):
        self.connection.close()
        logging.info("SQLite Pipeline closed")

    def process_item(self, item, spider):
        try:
            adapter = ItemAdapter(item)
            self.cursor.execute('''
            INSERT INTO transcripts (title, plot, full_script, url) VALUES (?, ?, ?, ?)
            ''', (
                adapter.get('title'),
                adapter.get('plot'),
                adapter.get('full_script'),
                adapter.get('url')
            ))
            self.connection.commit()
            logging.info(f"Item inserted successfully: {adapter.get('title')}")
        except sqlite3.Error as e:
            logging.error(f"Error while inserting item: {e}")
        return item
        