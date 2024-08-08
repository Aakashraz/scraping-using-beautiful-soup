from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('TWITTER_USER')
password = os.getenv('TWITTER_PASS')

print(type(username), password)

driver = webdriver.Chrome()
url = 'https://twitter.com/'
driver.get(url)
driver.maximize_window()

wait = WebDriverWait(driver, 20)
login = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//a[@data-testid = "loginButton"]'))
)
login.click()
time.sleep(2)

login_box = driver.find_element(By.XPATH, '//div[contains(@class, "css-175oi2r r-ywje51 r-nllxps r-jxj0sb r-1fkl15p r-16wqof")]')
user = WebDriverWait(login_box, 10).until(
    EC.presence_of_element_located((By.XPATH, './/input[@name = "text"]'))
)
user.send_keys(username)
driver.quit()