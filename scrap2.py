from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
url = 'https://www.audible.com/search'
driver.get(url)
wait = WebDriverWait(driver, 20)
# driver.maximize_window()

# for the container
container = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "adbl-impression-container")]')))
# find all product elements
products = container.find_elements(By.XPATH, './/li')

for product in products:
    try:
        runtime_element = WebDriverWait(product, 10).until(
            EC.presence_of_element_located((By.XPATH, './/li[contains(@class, "runtimeLabel")]'))
        )
        print(f"runtime: {runtime_element.text}")

        title_element = WebDriverWait(product, 10).until(
            EC.presence_of_element_located((By.XPATH, './/h3[contains(@class, "bc-heading")]'))
        )
        print(f"Title: {title_element.text}")
        print("----------------------")
    except TimeoutError:
        print("Couldn't find in the product")
    except Exception as e:
        print(f"AN ERROR OCCURRED: {e}")

driver.quit()
