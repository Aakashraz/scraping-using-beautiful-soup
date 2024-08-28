import scrapy


class WorldometersSpider(scrapy.Spider):
    name = "worldometers"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ['https://www.worldometers.info/world-population/population-by-country']

    def parse(self, response):
        # title = response.xpath('//h1/text()').get()
        countries = response.xpath('//td/a')

        for country in countries:
            country_name = country.xpath('.//text()').get()
            # the following will yield, what's inside the href attribute
            link = country.xpath('.//@href').get()

            # using absolute url rather than relative link
            # absolute_url = f'https://www.worldometers.info{link}'

            # the alternative code to the above line using urljoin()
            # absolute_url = response.urljoin(link)
            # yield scrapy.Request(url=absolute_url)

            # using relative url
            yield response.follow(url=link)

            # yield {
            #     'LINK': link,
            #     'countryName': country_name,
            # }
