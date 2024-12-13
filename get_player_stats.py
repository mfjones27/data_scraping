import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def write_to_csv(headers, cleaned_data):
    with open('playerStats.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(headers)
        writer.writerows(cleaned_data)
    print("CSV written successfully.")

def get_cleaned_data(driver, url):
    driver.get(url)
    time.sleep(5)  
    cookie_accept_btn = driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
    cookie_accept_btn.click()

    div = driver.find_element(By.XPATH, '//div[@class="mls-c-stats__table"]')
    table = div.find_element(By.TAG_NAME, 'table')
    headers = [th.text for th in table.find_elements(By.TAG_NAME, 'th') if th.text != '']

    data = []
    while True:
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            row_data = [col.text for col in cols]
            if row_data:
                data.append(row_data)
        
        btn = driver.find_element(By.XPATH, '//button[@aria-label="Next results"]')
        if btn.get_attribute('disabled'):
            break
        else:
            btn.click()
            time.sleep(5)

    cleaned_data = []
    for r in data:
        player = r[0]
        club = r[1]
        numericals = [int(val) if val.isdigit() else float(val) for val in r[2:]]
        cleaned_data.append([player, club]+numericals)

    return headers, cleaned_data


def main():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    service = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    url = 'https://www.mlssoccer.com/stats/players/#season=2024&competition=mls-regular-season&club=all&statType=general&position=all'
    
    try:
        headers, cleaned_data = get_cleaned_data(driver, url)
        write_to_csv(headers, cleaned_data)
    finally:
        driver.quit()


if __name__ == '__main__':
    main()