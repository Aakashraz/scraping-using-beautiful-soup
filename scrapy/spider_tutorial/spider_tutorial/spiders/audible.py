import scrapy


class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.com"]
    start_urls = ["https://www.audible.com/search"]

    # ancestor::li: This part checks if the current <li> has any <li> elements above it
    # in the hierarchy (i.e., if there are any <li> tags that are parents, grandparents, etc., of the current <li>).
    #
    # not(ancestor::li): This means "select only those <li> elements that do not have any <li> elements as ancestors."
    def parse(self, response):
        product_container = response.xpath('(//div[@class="adbl-impression-container "])[1]//li[not(ancestor::li)]')
        for product in product_container:
            book_title = product.xpath('.//h3/a/text()').get()
            book_author = product.xpath('.//li[contains(@class,"authorLabel")]/span/a/text()').get()
            book_runtime = product.xpath('.//li[contains(@class,"runtimeLabel")]/span/text()').get()
            release_date = product.xpath('.//li[contains(@class,"releaseDateLabel")]/span/text()').get()
            # to remove the whitespaces and new lines
            release_date = release_date.strip().replace('\n', '')
            release_date = ' '.join(release_date.split())
            release_date = release_date.replace('Release date:', '').strip()

            yield {
                'TITLE': book_title,
                'AUTHORS': book_author,
                'RUNTIME': book_runtime,
                'RELEASE DATE': release_date,
            }
