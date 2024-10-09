import scrapy
from scrapy_splash import SplashRequest


class AdamchoiSpider(scrapy.Spider):
    name = "adamchoi"
    allowed_domains = ["adamchoi.co.uk"]
    # start_urls = ["https://adamchoi.co.uk"]

    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(3))
            all_matches = assert(splash:select_all("label.btn.btn-sm.btn-primary"))
            all_matches[2]:mouse_click()
            assert(splash:wait(3))
            splash:set_viewport_full()
            return {
            splash:png(),
            splash:html()
            }
        end
    '''

    def start_requests(self):
        yield SplashRequest(url="https://www.adamchoi.co.uk/overs/detailed", callback=self.parse,
                            endpoint="execute", args={'lua_source': self.script})

    def parse(self, response):
        print(f'url-------------->>>>>>>>>>>>>>>>>>{response.url}')
        rows = response.xpath('//tr')
        print(type(rows))
        print(rows)
        # for row in rows[:4]:
        #     date = row.xpath('./td[1]/text()').get()
        #     home_team = row.xpath('./td[2]/text()').get()
        #     score = row.xpath('./td[3]/text()').get()
        #     away_team = row.xpath('./td[4]/text()').get()
        #     yield {
        #         'date': date,
        #         'home_team': home_team,
        #         'score': score,
        #         'away_team': away_team,
        #     }
