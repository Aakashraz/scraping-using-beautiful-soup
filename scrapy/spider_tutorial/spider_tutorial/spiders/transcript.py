import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptSpider(CrawlSpider):
    name = "transcript"
    allowed_domains = ["subslikescript.com"]
    # start_urls = ["https://subslikescript.com/movies_letter-X"]     # for less no of pages to crawl
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'

    # This is for the initial requests to kick off the spider and load the first page.
    # The spider starts by sending a request to https://subslikescript.com/movies_letter-X
    # with the custom User-Agent set in start_requests()
    def start_requests(self):
        yield scrapy.Request(
            url='https://subslikescript.com/movies_letter-X',
            headers={
                'User-Agent': self.user_agent
            },
        )

    # Key Concepts of rules:
    #
    #     LinkExtractor: Identifies which links to follow based on patterns (allow and deny).
    #     callback: Specifies the method to call when certain links are followed (e.g., parse_item).
    #     Rules: Define how the spider behaves when encountering links on the page (whether to follow or extract data).
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='scripts-list']/li/a"), callback="parse_item", follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//a[@rel='next'])[1]"), follow=True, process_request='set_user_agent'),
    )
    # Extracting the data from matching websites in the LinkExtractor is:
    #     Recursive Behavior: The process of following links and handling responses is recursive.
    #     It involves continuously fetching new pages, extracting data, and following further links.
    #
    #     Loop-like Process: Although not a literal loop, the process behaves similarly by continually
    #     handling new pages and links until the rules and constraints are met or there are no more links to follow.
    #
    # This systematic approach allows Scrapy to efficiently crawl and scrape large and complex websites.

    # Understanding the process_request inside the Rule:
    # The process_request method lets you modify each request before it is sent, enabling you to:
    #
    #     Set a custom User-Agent for every request.
    #     Add custom headers or cookies.
    #     Modify or log the request in some other way before it is sent.

    # Why This Is Important
    # Some websites block Scrapy or other bots, so setting a browser-like User-Agent helps
    # your spider avoid detection and reduces the chances of being blocked by the website.

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request
    # This is for all subsequent requests generated automatically by Scrapy when following links
    # (like the "next" page). You want to ensure that all those subsequent requests also use the correct User-Agent.

    def parse_item(self, response):
        article = response.xpath('//article[@class="main-article"]')
        # print(response.url)
        # This converts the byte string back to a regular string (str) in Python, which will not display the b prefix when printed.
        user_agent_str = response.request.headers['User-Agent'].decode('utf-8')
        yield {
            'title': article.xpath('./h1/text()').get().split('-')[0],
            'plot': article.xpath('./p/text()').get(),
            # 'Full-Script': article.xpath('./div[@class="full-script"]/text()').getall(),
            'URL': response.url,
            'USER-AGENT': user_agent_str,
        }
