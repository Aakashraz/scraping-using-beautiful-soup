import scrapy


class Mp3DownloaderSpider(scrapy.Spider):
    name = 'mp3_downloader'
    start_urls = ['https://pixabay.com/music/search/']

    def parse(self, response):
        pass