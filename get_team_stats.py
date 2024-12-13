import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def write_to_csv(headers, data):
    with open('teamStats.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(headers)
        writer.writerows(data)
    print('CSV written successfully')

def get_cleaned_data(driver, url):
    driver.get(url)
    time.sleep(5)
    cookie_accept_btn = driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
    cookie_accept_btn.click()

    div = driver.find_element(By.XPATH, '//div[@class="mls-c-stats__table"]')
    table = div.find_element(By.TAG_NAME, 'table')
    headers = [th.text for th in table.find_elements(By.TAG_NAME, 'th') if th.text != '']
    rows = table.find_elements(By.TAG_NAME, 'tr')

    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'td')
        row_data = [col.text for col in cols]
        if row_data:
            club = row_data[0]
            if club == 'TBC':
                continue
            numericals = [int(val) if val.isdigit() else float(val) for val in row_data[1:] if val != '']
            data.append([club]+numericals)

    return headers, data


def main():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    service = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    url = 'https://www.mlssoccer.com/stats/clubs/#season=2024&competition=mls-regular-season&statType=general'

    try:
        headers, data = get_cleaned_data(driver, url)
        write_to_csv(headers, data)
    finally:
        driver.quit()

if __name__ == '__main__':
    main()