import scrapy


class Mp3DownloaderSpider(scrapy.Spider):
    name = 'mp3_downloader'
    start_urls = ['https://www.songspk2.info/indian_movie/MereSapnonKiRani-1997.html']

    def parse(self, response):
        pass