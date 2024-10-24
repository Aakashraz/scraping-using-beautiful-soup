import time

import requests
from bs4 import BeautifulSoup

base_url = 'https://www.thewhiskyexchange.com/'

# To bypass the security, this long headers content is used, because access was denied before from the website.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'DNT': '1',  # Do Not Track Request Header
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}

product_links = []
# the for loop is used for the pagination.
for x in range(1, 6):
    time.sleep(3)

    r = requests.get(f'https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={x}', headers=headers, timeout=5)
    if r.status_code == 200:
        content = r.content
        soup = BeautifulSoup(content, 'lxml')

        # to check there is incoming response from the website
        # print(f"Response Status Code:{r.status_code}\n")

        product_list = soup.find_all("li", class_="product-grid__item")
        for product in product_list:
            for link in product.find_all('a', href=True):
                product_links.append(base_url + link['href'])

        print(f"product length: {len(product_links)}")
print(f'Product links: {product_links}')