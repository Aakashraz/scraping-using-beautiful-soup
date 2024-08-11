from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
import os
from dotenv import load_dotenv

load_dotenv(override=True)  # override the value in the .env file

username = os.getenv('TWITTER_USER')
password = os.getenv('TWITTER_PASS')

print(type(username), username, password)

chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=chrome_options)
url = 'https://twitter.com/'
driver.get(url)
driver.maximize_window()

wait = WebDriverWait(driver, 20)

# ----------------------------------    SIGN IN ------------------------------------
try:
    login = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//a[@data-testid = "loginButton"]'))
    )
    login.click()
    time.sleep(3)
except:
    print('Login failed')

try:
    login_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.css-175oi2r.r-ywje51.r-nllxps.r-jxj0sb.r-1fkl15p.r-16wqof"))
    )
    user_input = login_box.find_element(By.XPATH, './/input[@name="text"]')
    user_input.send_keys(username)
    # time.sleep(2)
    print('Username successful')
    next_button = WebDriverWait(login_box, 10).until(
        EC.visibility_of_element_located((By.XPATH,
                                          './/button[contains(@class, "css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-ywje51 r-184id4b r-13qz1uu r-2yi16 r-1qi8awa r-3pj75a r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l")]'))
    )
    print("Next button found: ", next_button)
    time.sleep(1)
    next_button.click()
    print("Next button clicked...")

    # this input is used to bypass the twitter captcha/authentication.
    input("Press Enter after completing the authentication...")


except Exception as e:
    print(e)

driver.quit()
