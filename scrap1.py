from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
url = 'https://www.adamchoi.co.uk/overs/detailed'
driver.get(url)

all_matches = driver.find_element(By.XPATH, 'label[@analytics-event="All matches"]')
all_matches.click()

time.sleep(2)

driver.quit()