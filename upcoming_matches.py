import re
from datetime import datetime as dt
from playwright.sync_api import sync_playwright

def get_schedule(divs):
    current_year = dt.now().year
    matches = []
    for div in divs:
        match_data = [value for value in div.inner_text().split('\n') if value]
        if 'Final' in match_data:
            continue
        
        match = {
            'Datetime': dt.strptime(f'{current_year}/{f'{match_data[0]} {match_data[2]}'}', '%Y/%m/%d %I:%M%p').isoformat(),
            'teamA': re.sub(r'\(.*?\)', '', match_data[1]).strip(),
            'teamB': re.sub(r'\(.*?\)', '', match_data[3]).strip(),
            'Comp': f'{match_data[5]}',
            'Venue': match_data[7]
        }
        matches.append(match)

    matches = sorted(matches, key=lambda x: dt.strptime(x['Datetime'], "%Y-%m-%dT%H:%M:%S"))
    print(matches)
    return matches

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  
        page = browser.new_page()
        page.goto('https://www.mlssoccer.com/schedule/scores', wait_until='domcontentloaded')

        try:
            page.wait_for_selector('div.sc-jTjUTQ', timeout=10000)
            divs = page.query_selector_all('div.sc-jTjUTQ')
            options = page.query_selector_all('option.mls-o-buttons__dropdown-item')

            if divs and options:
                teams = [option.inner_text() for option in options[16:45]]
                return get_schedule(divs), teams
            else:
                print("No divs found with the class 'sc-jTjUTQ'.")
        except Exception as e:
            print(f"An error occurred: {e}")

        browser.close()