import csv
import requests
from bs4 import BeautifulSoup

# url = requests.get('https://quotes.toscrape.com/')
# contents = url.content
# # print(contents)
#
# # copying the content into beautiful soup
# soup = BeautifulSoup(contents, 'html.parser')
# # print("\n\n", soup)
# quotes = soup.find_all("span", {"class": "text"})
# authors = soup.find_all("small", {"class": "author"})
#
# with open('scraped_quotes.csv', 'w') as file:
#     writer = csv.writer(file)
#     # csv.writer(file): This function creates an object that you can use to write to a CSV file.
#     # It takes a file object as an argument.
#     writer.writerow(['Quote', 'Author'])
#     # ['Quote', 'Author']: This is a list representing a single row.
#     # Each element of the list corresponds to a column in the CSV file.
#     # Header Row: This row acts as the header, providing column names for the data that will be written subsequently.
#     # Headers are optional but useful for understanding the structure of the data.
#
#     for quote, author in zip(quotes, authors):
#         print(f"{quote.text} - {author.text}")
#         writer.writerow([quote.text, author.text])

# The zip() function takes multiple iterables (like lists or tuples) and combines them into a single iterator of tuples.
# Each tuple contains elements from the iterables at the same position.
# Example:
# Suppose quotes = ["Quote1", "Quote2"] and authors = ["Author1", "Author2"].
#
#     zip(quotes, authors) produces:
#         First iteration: ("Quote1", "Author1")
#         Second iteration: ("Quote2", "Author2")



# --------------------  Using Selenium  --------------------------

from selenium import webdriver
import time
import getpass

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()
driver.get('https://quotes.toscrape.com/')

login_page = driver.find_element(By.LINK_TEXT, 'Login').click()
username_input = driver.find_element(By.ID, 'username')
password_input = driver.find_element(By.ID, 'password')
username_input.send_keys("admin")
my_password = getpass.getpass(prompt='Enter your password: ')
password_input.send_keys(my_password)
driver.find_element(By.CSS_SELECTOR, 'input.btn.btn-primary').click()

# Open the CSV file for writing with UTF-8 encoding
with open("scraped_quotes.csv", "w", newline="\n", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['QUOTES Using Selenium', 'AUTHORS Using Selenium'])
    while True:
        quotes = driver.find_elements(By.CLASS_NAME, 'text')
        authors = driver.find_elements(By.CLASS_NAME, 'author')

        for quote, author in zip(quotes, authors):
            print(quote.text, author.text)
            writer.writerow([quote.text, author.text])
        # Try to find and click the 'Next' button to go to the next page
        try:
            next_button = driver.find_element(By.PARTIAL_LINK_TEXT, 'Next')
            next_button.click()
        except NoSuchElementException:
            break

driver.quit()