from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

# Instantiating the Options() object
chrome_option = Options()

# chrome_option setting customized
# 'headless' mode is that which work without opening the Chrome browser
# By commenting the 'headless' option, we can avoid the issue related to
#  Content Security Policy (CSP) restrictions of the Audible website,

# chrome_option.add_argument('--headless')
chrome_option.add_argument('--window-size=1920x1080')

driver = webdriver.Chrome(options=chrome_option)
url = 'https://www.audible.com/search'
driver.get(url)
wait = WebDriverWait(driver, 10)
# driver.maximize_window()

# pagination handling
pagination = driver.find_element(By.XPATH, '//ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements(By.TAG_NAME, 'li')

last_page = int(pages[-2].text)
print(f"Last page: {last_page}")

current_page = 1

book_title = []
book_runtime = []
book_author = []
book_release_date = []

while current_page <= last_page:
    # for the container
    container = wait.until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "adbl-impression-container")]'))
    )
    # find all product elements
    products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')

    for product in products:
        try:
            title_element = WebDriverWait(product, 5).until(
                EC.presence_of_element_located((By.XPATH, './/h3[contains(@class, "bc-heading")]'))
            )
            print(title_element.text)
            book_title.append(title_element.text)

            author_element = WebDriverWait(product, 5).until(
                EC.presence_of_element_located((By.XPATH, './/li[contains(@class, "authorLabel")]'))
            )
            print(author_element.text)
            book_author.append(author_element.text)

            runtime_element = WebDriverWait(product, 5).until(
                EC.presence_of_element_located((By.XPATH, './/li[contains(@class, "runtimeLabel")]'))
            )
            print(f"runtime: {runtime_element.text}")
            book_runtime.append(runtime_element.text)

            release_element = WebDriverWait(product, 5).until(
                EC.presence_of_element_located((By.XPATH, './/li[contains(@class, "releaseDateLabel")] '))
            )
            print(release_element.text)
            book_release_date.append(release_element.text)
            print("----------------------")

        except TimeoutException:
            print("Couldn't find in the product")
        except Exception as e:
            print(f"AN ERROR OCCURRED: {e}")

    current_page = current_page + 1
    # this try except, block is used again to avoid the error:
    # Error Encountered:
    # The script crashed with a StaleElementReferenceException
    # when trying to find the next button to navigate to the third page.
    try:
        next_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(@class, "nextButton")]'))
        )
        # next_page_button = driver.find_element(By.XPATH, '//span[contains(@class, "nextButton")]')
        next_button.click()
    except TimeoutException:
        print("Couldn't find the next page")

driver.quit()

df = pd.DataFrame(
    {'Title': book_title, 'Author': book_author, 'Length': book_runtime, 'ReleaseDate': book_release_date, '': "\n-------------------------------------\n"})
df.to_csv('audible_books.csv', index=False)
