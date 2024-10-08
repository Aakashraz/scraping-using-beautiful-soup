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
        return [Request(u, meta={'bookname': item.get('book_name')}) for u in urls]

    # If you wanted to add extra parameters to the requests, like headers
    # or metadata, you could modify this method. For example:

    # def get_media_requests(self, item, info):
    #   urls = item.get(self.images_urls_field, [])
    #   return [Request(u, headers={'User-Agent': 'MyBot}, meta={'item':item}) for u in urls]

    # This would add a custom User-Agent to each request and
    # include the original item in the request's metadata.

    def file_path(self, request, response=None, info=None):
        # Get the bookname from the request's metadata
        bookname = request.meta.get('bookname', 'unknown')
        # Clean the bookname to make it suitable for a filename
        book_name = self.clean_bookname(bookname)
        return f"full/{book_name}.jpg"

    def clean_bookname(self, bookname):
        # Remove or replace characters that are unsafe for filenames
        unsafe_chars = '<>:"/\\|?*'
        for char in unsafe_chars:
            bookname = bookname.replace(char, '_')
        # Limit the length of the bookname to avoid issues with long filenames
        return bookname[:100]

    # Illustration of this method with an example:
    # Suppose we have a book name: "Alice's Adventures in Wonderland: A Classic Tale?"
    # The method will process this string as follows:
    #
    # It will first replace the : with _
    # Result: "Alice's Adventures in Wonderland_ A Classic Tale?"
    # Then it will replace the ? with _
    # Final result: "Alice's Adventures in Wonderland_ A Classic Tale_"
    #
    # If we had a more problematic title like "Alice/Wonderland: A <Tale> of Wonder?*", the process would be:
    #
    # Replace / → "Alice_Wonderland: A <Tale> of Wonder?*"
    # Replace : → "Alice_Wonderland_ A <Tale> of Wonder?*"
    # Replace < → "Alice_Wonderland_ A _Tale> of Wonder?*"
    # Replace > → "Alice_Wonderland_ A _Tale_ of Wonder?*"
    # Replace ? → "Alice_Wonderland_ A _Tale_ of Wonder_*"
    # Replace * → "Alice_Wonderland_ A _Tale_ of Wonder__"
