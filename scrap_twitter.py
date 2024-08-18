from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

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
# driver.maximize_window()

wait = WebDriverWait(driver, 20)
url = 'https://twitter.com/'


# ----------------------------------    SIGN IN ------------------------------------

def login_twitter(dr, user, key, max_retries=3, delay=5):
    for attempt in range(max_retries):
        dr.get(url)

        try:
            login = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//a[@data-testid = "loginButton"]'))
            )
            login.click()
            time.sleep(2)
        except:
            print('Login failed')

        try:
            login_box = WebDriverWait(dr, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div.css-175oi2r.r-ywje51.r-nllxps.r-jxj0sb.r-1fkl15p.r-16wqof"))
            )
            user_input = login_box.find_element(By.XPATH, './/input[@name="text"]')
            user_input.send_keys(user)
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
            time.sleep(3)

            # Pause for manual authentication after entering username
            input("Please complete any authentication steps if required, "
                  "then press enter to continue...")

            password_input = WebDriverWait(dr, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//input[@name= "password"]'))
            )
            password_input.send_keys(key)
            time.sleep(2)

            login_button = dr.find_element(By.XPATH, '//button[@data-testid="LoginForm_Login_Button"]')
            login_button.click()
            time.sleep(10)
            print('Login Successful')
            return True

            # this input is used to bypass the twitter captcha/authentication.
            # input("Press Enter after completing the authentication...")

        except (TimeoutException, NoSuchElementException) as e:
            print(f"Login attempt {attempt +1} failed: {str(e)}")
            if attempt < max_retries-1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Login failed")
                return False


# ------------------------------------------ QUERY SEARCH DATA -------------------------------------

if login_twitter(driver, username, password):
    try:
        url_query = 'https://x.com/search?q=python&src=typed_query'
        driver.get(url_query)
        time.sleep(3)
        timeline_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@aria-label,"Timeline: Search")]'))
        )
        print(f"Timeline found: {timeline_box}\n\n")
        tweets = WebDriverWait(timeline_box, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, './/div[@data-testid="cellInnerDiv"]'))
        )
        print(f"Tweets found: {tweets.text}\n\n")

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

else:
    print('Unable to log in to Twitter (may be due to twitter authentication rule),'
          'either please check your credentials or try again later')


driver.quit()

# pd.DataFrame({'user': user_id_data})
