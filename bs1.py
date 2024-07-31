import requests
from bs4 import BeautifulSoup

base_url = 'https://subslikescript.com'
response = requests.get(base_url)
contents = response.content
soup = BeautifulSoup(contents, 'html.parser')

main_page = soup.find('main', {'class': 'mainpage'})
articles = main_page.findAll('article')
print(type(articles))
links = []
# for article in articles:
#     anchors = article.findAll('a')
#     for a in anchors:
#         link = a.get('href').strip()
#         links.append(link)
# BOTH THE ABOVE FOR LOOP AND THE BELOW HAVE SAME OUTPUT-------------
for link in articles.findAll('a', href=True):
    links.append(link['href'])
# print(links)

for i in links:
    url = base_url + i
    print(url)

    response = requests.get(url)
    contents = response.content
    soup = BeautifulSoup(contents, 'html.parser')
    title = soup.find('h1')
    plot = soup.find('p', {"class": "plot"})
    scripts = soup.find('div', {"class": "full-script"}).text
    print(f"Title: {title}")
    print(f"Plot: {plot} \n Scripts: {scripts}\n\n")