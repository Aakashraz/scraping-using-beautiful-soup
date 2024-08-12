from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)
url = 'https://x.com/search?q=olympics&src=typed_query&f=top'
driver.get(url)

tweets = driver.find_elements(By.XPATH, '//div[contains(@aria-label,"Timeline: Search")]')

for tweet in tweets:
    print(tweet)