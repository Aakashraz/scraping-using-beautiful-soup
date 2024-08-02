from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

driver = webdriver.Chrome()
url = 'https://www.adamchoi.co.uk/overs/detailed'
driver.get(url)

all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
all_matches_button.click()

time.sleep(2)

matches = driver.find_elements(By.TAG_NAME, 'tr')
match_day = []
home_team = []
final_result = []
away_team = []

for match in matches:
    match_day.append((match.find_element(By.XPATH, './td[1]')).text)
    home_team.append((match.find_element(By.XPATH, './td[2]')).text)
    final_result.append((match.find_element(By.XPATH, './td[3]')).text)
    away_team.append((match.find_element(By.XPATH, './td[4]')).text)

driver.quit()

df = pd.DataFrame({'Date': match_day, 'Home Team': home_team, 'Score': final_result, 'Away Team': away_team})
# to skip the index, it is set to False
df.to_csv('all_matches.csv', index=False)
print(df)