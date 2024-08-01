import requests
from bs4 import BeautifulSoup
import csv


def get_details(sites):
    response_details = requests.get(sites)
    contents_details = response_details.content
    soup_details = BeautifulSoup(contents_details, 'html.parser')
    title_details = soup_details.find('h1').text
    plot_details = soup_details.find('p', {"class": "plot"}).text
    scripts_details = soup_details.find('div', {"class": "full-script"}).text
    print(f"Title: {title_details}")
    print(f"Plot: {plot_details} \n Transcripts: {scripts_details}\n\n")
    return title_details, plot_details, scripts_details


base_url = 'https://subslikescript.com'
response = requests.get(base_url)
contents = response.content
soup = BeautifulSoup(contents, 'html.parser')

main_page = soup.find('main', {'class': 'mainpage'})
articles = main_page.findAll('article')

# the below list of high_rated_series_links is for the last article only
high_rated_series = articles[3].findAll('a', href=True)
high_rated_series_links = [a['href'] for a in high_rated_series]
print(f"High Rated Series: {high_rated_series_links}")
# print(articles[3])

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

# This loop is for getting all the links inside anchor tags of the main page
for link in main_page.findAll('a', href=True):
    links.append(link['href'])
# print(f"ALl Links: {links}")


with open('subsscripts.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Plot', 'Transcripts'])
    for i in links[2:]:
        links_season = []
        # remember to reset the links_season[] array, for links in high_rated_series_links,
        # otherwise it will append the data from the beginning again and again
        try:
            if i.startswith('/'):
                print(f"i:{i}")
                if i not in high_rated_series_links:
                    url = base_url + i
                    # # if i.startswith('/movie'):
                    # # It works only for first three(3) articles only
                    title, plot, transcripts = get_details(url)
                    writer.writerow([title, plot, transcripts])
                    print(f"url:{url}\n not in high Rated Series: {i}")

                elif i in high_rated_series_links:
                    # to fetch all the div elements containing anchor tags of all seasons available on the page
                    # after matching the url, it will open a new link by appending the links to base_url
                    # then, it will fetch the data about the series (all seasons available there) from that opened link
                    series_url = base_url + i
                    res = requests.get(series_url)
                    cont = res.content
                    soup_series = BeautifulSoup(cont, 'html.parser')
                    series_seasons = soup_series.find_all('div', class_='series_seasons')
                    # print(f"series_seasons {series_seasons}")
                    # to get all the href:links inside the anchor tags
                    for season in series_seasons:
                        anchors = season.find_all('a', href=True)
                        # print(f"anchors: {anchors}")

                        # to add the accessed href links to the base URL
                        for anchor in anchors:
                            links_season.append(base_url + anchor['href'])

                    print(f"total season episode: {len(links_season)} Seasons: {links_season}")

                    # to get the details by running the loop inside each season
                    for link in links_season:
                        title, plot, transcripts = get_details(link)
                        writer.writerow([title, plot, transcripts])
                        print(f"link: {link}")

        except Exception as e:
            print(e)
