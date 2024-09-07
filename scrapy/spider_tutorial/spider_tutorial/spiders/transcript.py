import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptSpider(CrawlSpider):
    name = "transcript"
    allowed_domains = ["subslikescript.com"]
    start_urls = ["https://subslikescript.com/movies_letter-Z"]     # for less no of pages to crawl

    # Key Concepts:
    #
    #     LinkExtractor: Identifies which links to follow based on patterns (allow and deny).
    #     callback: Specifies the method to call when certain links are followed (e.g., parse_item).
    #     Rules: Define how the spider behaves when encountering links on the page (whether to follow or extract data).
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='scripts-list']/li/a"), callback="parse_item", follow=True),
        Rule(LinkExtractor(restrict_xpaths="(//a[@rel='next'])[1]"), follow=True),
    )
    # Extracting the data from matching websites in the LinkExtractor is:
    #     Recursive Behavior: The process of following links and handling responses is recursive.
    #     It involves continuously fetching new pages, extracting data, and following further links.
    #
    #     Loop-like Process: Although not a literal loop, the process behaves similarly by continually
    #     handling new pages and links until the rules and constraints are met or there are no more links to follow.
    #
    # This systematic approach allows Scrapy to efficiently crawl and scrape large and complex websites.

    def parse_item(self, response):
        article = response.xpath('//article[@class="main-article"]')
        # print(response.url)
        yield {
            'title': article.xpath('./h1/text()').get().split('-')[0],
            'plot': article.xpath('./p/text()').get(),
            # 'Full-Script': article.xpath('./div[@class="full-script"]/text()').getall(),
            'URL': response.url,
        }
