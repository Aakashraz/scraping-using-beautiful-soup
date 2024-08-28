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
            yield response.follow(url=link, callback=self.parse_country, meta={'country': country_name})

            # Summary
            #
            # self is necessary to reference the instance of the class within which methods and variables are defined.
            # It allows methods to modify the object’s state or access other attributes and methods.
            # In Scrapy, using self ensures that Scrapy calls the correct instance method when it receives a response.

            # yield {
            #     'LINK': link,
            #     'countryName': country_name,
            # }

    def parse_country(self, response):
        # this country name is fetched from the meta (data) from country inside the for loop of parse() method
        country_name_from_meta = response.request.meta['country']
        rows = response.xpath("(//table[contains(@class,'table')])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()

            yield {
                'Country Name': country_name_from_meta,
                'Year': year,
                'Total Population': population,
            }
