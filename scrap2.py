from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
import time

option = Options
option.headless = True
option.add_argument('window-size=1920x1080')

driver = webdriver.Chrome(options=option)
url = 'https://www.audible.com/search'
driver.get(url)
wait = WebDriverWait(driver, 20)
# driver.maximize_window()

# for the container
container = wait.until(
    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "adbl-impression-container")]'))
)
# find all product elements
products = container.find_elements(By.XPATH, './/li')
# book_title = []
# book_runtime = []

for product in products:
    try:
        runtime_element = WebDriverWait(product, 5).until(
            EC.presence_of_element_located((By.XPATH, './/li[contains(@class, "runtimeLabel")]'))
        )
        print(f"runtime: {runtime_element.text}")

        title_element = WebDriverWait(product, 5).until(
            EC.presence_of_element_located((By.XPATH, './/h3[contains(@class, "bc-heading")]'))
        )
        print(f"Title: {title_element.text}")

        # book_title.append(product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text)
        # book_runtime.append(product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)
        print("----------------------")

    except TimeoutError:
        print("Couldn't find in the product")
    except Exception as e:
        print(f"AN ERROR OCCURRED: {e}")

driver.quit()
