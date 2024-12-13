import json
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def get_match_results(url, driver):
    driver.get(url)
    time.sleep(5)
    try:
        cookie_accept_btn = driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
        cookie_accept_btn.click()
    except NoSuchElementException:
        pass


    div = driver.find_element(By.XPATH, '//div[@class="mls-c-standings-form-guide__table"]')
    table = div.find_element(By.TAG_NAME, 'table')
    headers = [header.text for header in table.find_elements(By.TAG_NAME, 'th') if header.text != '']
    trs = table.find_elements(By.TAG_NAME, 'tr')
    
    
    rows = list()
    for tr in trs:
        cols = [col.text for col in tr.find_elements(By.TAG_NAME, 'td') if col.text != '']
        if cols == []:
            continue
        rows.append(cols)

    cleaned_data = []

    for row in rows:
        rank = row[0]
        club = row[1]
        match_results = []
        for count, match in enumerate(row[2:]):
            parts = match.split('\n')
            if len(parts) == 3:
                match_result = {
                    'match': count+1,
                    'res': parts[0],
                    'opp': parts[1],
                    'scr': parts[2]
                }
                match_results.append(match_result)
            elif len(parts) == 1:
                match_result = {
                    'match': count+1,
                    'opp': parts[0],
                }
                match_results.append(match_result)
        team_dict = {
            'Rank': rank,
            'Club': club,
            'Match_Results': match_results
        }

        cleaned_data.append(team_dict)
    
    return cleaned_data

def write_csv(cd):
    df = pd.DataFrame(cd)
    df.set_index('Rank', inplace=True)
    df['Match_Results'] = df['Match_Results'].apply(lambda x: json.dumps(x))
    df.to_csv('matchStats.csv')

def main():
    chrome_options = Options()
    chrome_options.add_argument(r'user-data-dir=C:/Users/mfjon/AppData/Local/Google/Chrome/User Data')
    #chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)
    url = 'https://www.mlssoccer.com/standings/form-guide/?year=2024'
    try:
        cd = get_match_results(url, driver)
        write_csv(cd)
    finally:
        driver.quit()
    return

if __name__ == '__main__':
    main()