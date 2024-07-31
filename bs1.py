import requests
from bs4 import BeautifulSoup

base_url = 'https://subslikescript.com'
response = requests.get(base_url)
contents = response.content
soup = BeautifulSoup(contents, 'html.parser')

main_page = soup.find('main', {'class': 'mainpage'})
articles = main_page.findAll('article')
# print(articles[1])
links = []
# for article in articles:
#     anchors = article.findAll('a')
#     for a in anchors:
#         link = a.get('href').strip()
#         links.append(link)
# BOTH THE ABOVE FOR LOOP AND THE BELOW HAVE SAME OUTPUT-------------
# BELOW IS EXAMPLE USING LIST COMPREHENSION TO GET ALL THE LINKS-------
# links = [link['href'] for link in main_page.findAll('a', href=True)]
# ------------------------------------------------------------------

for link in main_page.findAll('a', href=True):
    links.append(link['href'])
print(f"ALl Links: {links}")

for i in links[2:]:
    links_season = []

    try:
        if i.startswith('/'):
            url = base_url + i
            print(url)

            response = requests.get(url)
            contents = response.content
            soup = BeautifulSoup(contents, 'html.parser')

            # if i.startswith('/movie'):
            #     title = soup.find('h1').text
            #     plot = soup.find('p', {"class": "plot"}).text
            #     scripts = soup.find('div', {"class": "full-script"}).text
            #     print(f"Title: {title}")
                # print(f"Plot: {plot}")
                # print(f"\n Transcripts: {scripts}\n\n")
            if i.startswith('/series'):
                seasons = soup.findAll('div', class_='season')
                for season in seasons:
                    anchors = season.find_all('a', href=True)
                    for anchor in anchors:
                        links_season.append(base_url + anchor['href'])

                for link in links_season:
                    response = requests.get(link)
                    contents = response.content
                    soup = BeautifulSoup(contents, 'html.parser')
                    title = soup.find('h1').text
                    plot = soup.find('p', {"class": "plot"}).text
                    scripts = soup.find('div', {"class": "full-script"}).text
                    print(f"Title: {title}")

            print(f"Seasons: {links_season}")

    except Exception as e:
        print(e)