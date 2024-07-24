import csv
import requests
from bs4 import BeautifulSoup

url = requests.get('https://quotes.toscrape.com/')
contents = url.content
# print(contents)

# copying the content into beautiful soup
soup = BeautifulSoup(contents, 'html.parser')
# print("\n\n", soup)
quotes = soup.find_all("span", {"class": "text"})
authors = soup.find_all("small", {"class": "author"})

with open('scraped_quotes.csv', 'w') as file:
    writer = csv.writer(file)
    # csv.writer(file): This function creates an object that you can use to write to a CSV file.
    # It takes a file object as an argument.
    writer.writerow(['Quote', 'Author'])
    # ['Quote', 'Author']: This is a list representing a single row.
    # Each element of the list corresponds to a column in the CSV file.
    # Header Row: This row acts as the header, providing column names for the data that will be written subsequently.
    # Headers are optional but useful for understanding the structure of the data.

    for quote, author in zip(quotes, authors):
        print(f"{quote.text} - {author.text}")
        writer.writerow([quote.text,  author.text])
