import scrapy
from scrapy_splash import SplashRequest


class AdamchoiSpider(scrapy.Spider):
    name = "adamchoi"
    allowed_domains = ["adamchoi.co.uk"]
    # start_urls = ["https://adamchoi.co.uk"]
    custom_settings = {
        'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }

    script = '''
        function main(splash, args)
            splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/127.0.0.0")
            splash.private_mode_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(3))
            all_matches = assert(splash:select_all("label.btn.btn-sm.btn-primary"))
            all_matches[2]:mouse_click()
            assert(splash:wait(3))
            splash:set_viewport_full()
            return splash:html()
        end
    '''
    # cannot use the following return statement because it yields the ValueError as
    # return {
    #     splash:html(),
    #     splash:png()
    # }
    # ValueError: Cannot use xpath on a Selector of type 'json'

    def start_requests(self):
        yield SplashRequest(url="https://www.adamchoi.co.uk/overs/detailed", callback=self.parse,
                            endpoint="execute", args={'lua_source': self.script})

    def parse(self, response):
        print(f'body-------------->>>>>>>>>>>>>>>>>>{type(response.body)}')
        print(f'USER-AGENT------>>>>>{response.request.headers.get('User-Agent')}')
        rows = response.xpath('//tr[contains(@class,"HighlightedRow")]')
        for row in rows:
            # print(type(row))
            # print(row)
            date = row.xpath('./td[1]/text()').get()
            home_team = row.xpath('./td[2]/text()').get()
            score = row.xpath('./td[3]/text()').get()
            away_team = row.xpath('./td[4]/text()').get()
            yield {
                'date': date,
                'home_team': home_team,
                'score': score,
                'away_team': away_team,
            }
