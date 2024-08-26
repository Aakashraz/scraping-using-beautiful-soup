import scrapy


class WorldometersSpider(scrapy.Spider):
    name = "worldometers"
    allowed_domains = ["www.worldometers.info/"]
    start_urls = ['https://www.worldometers.info/world-population/population-by-country']

    def parse(self, response):
        # title = response.xpath('//h1/text()').get()
        countries = response.xpath('//td/a')

        for country in countries:
            country_name = country.xpath('.//text()').get()
            # the following will yield, what's inside the href attribute
            link = country.xpath('.//@href').get()

            yield {
                'link': link,
                'countryName': country_name,
            }
