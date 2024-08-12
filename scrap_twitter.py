from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv(override=True)  # override the value in the .env file

username = os.getenv('TWITTER_USER')
password = os.getenv('TWITTER_PASS')

print(type(username), username, password)

chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)
url = 'https://twitter.com/'
driver.get(url)
# driver.maximize_window()

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
    time.sleep(2)

    password_input = driver.find_element(By.XPATH, '//input[@name= "password"]')
    password_input.send_keys(password)
    time.sleep(2)

    login_button = driver.find_element(By.XPATH, '//button[@data-testid="LoginForm_Login_Button"]')
    login_button.click()
    time.sleep(5)
    print('Login Successful')

    # this input is used to bypass the twitter captcha/authentication.
    # input("Press Enter after completing the authentication...")

except Exception as e:
    print(e)

# ------------------------------------------ QUERY SEARCH DATA -------------------------------------

try:
    url_query = 'https://x.com/search?q=python&src=typed_query'
    driver.get(url_query)
    time.sleep(5)
    # timeline_box = driver.find_element(By.XPATH, '//div[contains(@aria-label,"Timeline: Search")]')
    tweets = driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')

    user_id_data = []
    # tweet_text = []
    for tweet in tweets:
        # if tweet.text != '' or tweet.text != 'View all' or tweet.text == 'Discover more':
        user_id = tweet.find_element(By.XPATH, './/span[contains(text(), "@")]').text
        # check whether the span element exists or not for all the tweet
        print(f"userID: {user_id}")
        # tweet_text = tweet.find_element()
        # print("-----------------------------\n")
        # user_id_data.append(user_id)

    print(f"IDs: {user_id_data}")

except:
    pass

driver.quit()

# pd.DataFrame({'user': user_id_data})
