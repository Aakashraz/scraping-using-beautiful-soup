import scrapy
import re


class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.com"]
    start_urls = ["https://www.audible.com/search"]

    # def __init__(self):
    #     self.counter = 0

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
            # to remove the whitespaces and new lines from release date
            if release_date:
                release_date = release_date.strip().replace('\n', '')
                release_date = ' '.join(release_date.split())
                release_date = release_date.replace('Release date:', '').strip()

            yield {
                'TITLE': book_title,
                'AUTHORS': book_author,
                'RUNTIME': book_runtime,
                'RELEASE DATE': release_date,
            }

        pagination = response.xpath('//ul[contains(@class, "pagingElements")]')
        next_page_url = pagination.xpath('.//span[contains(@class, "nextButton")]/a/@href').get()
        print(f'next_page_url:..................{next_page_url}')
        print(f'response.url:>>>>>>>>>>> {response.url}')

        # Get the current page number using regular expression
        # to search for 'page=' followed by digits
        current_page = None
        match = re.search(r'page=(\d+)', next_page_url)

        # Extract the captured group (the digits after 'page=')
        if match:
            current_page = int(match.group(1))
            print(f'Current page: >>>>>>>>>>{current_page}')
        else:
            print("Page no. not found in the URL.")

        # Get the last page number and use a default value if not found
        try:
            last_page_element = pagination.xpath('(.//a[contains(@class, "pageNumberElement")])[last()]/text()').get()
            print(f'last_page_element>>>>>>>>>>>>>{last_page_element}')
            last_page = int(last_page_element) if last_page_element.isdigit() else 25
            print(f'last page no:>>>>>>> {last_page}, type>>>>>>>: {type(last_page)}')
        except (AttributeError, ValueError):
            last_page = 25
            print('Failed to extract last page number, hence using default as 100')

        # While conditional checking, to prevents the UnboundLocalError by checking if current_page
        # has been assigned a value from the URL before using it in the comparison.
        # Ensuring current_page is not None
        if current_page is not None and current_page-1 <= last_page:
            yield response.follow(url=next_page_url, callback=self.parse)
        else:
            print("Reached the last page or no more page available.................")
