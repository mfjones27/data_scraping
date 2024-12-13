import time
import requests as rq
import pandas as pd
pd.set_option('display.max_columns', None)

from io import StringIO
from bs4 import BeautifulSoup

years = list(range(2024,2018,-1))
standings_url = 'https://fbref.com/en/comps/22/Major-League-Soccer-Stats'
seasons = []

for year in years:
    print(year)
    data = rq.get(standings_url)
    soup = BeautifulSoup(data.text, 'html.parser')
    eastern_table = soup.select(f'#results{year}221Eastern-Conference_overall')[0]
    western_table = soup.select(f'#results{year}221Western-Conference_overall')[0]

    team_urls = [l.get('href') for l in eastern_table.find_all('a')+western_table.find_all('a') if '/squads/' in l.get('href')]
    previous_season = soup.select('a.prev')[0].get('href')
    standings_url = f'https://fbref.com{previous_season}'
    time.sleep(2)

    for url in team_urls:
        html = rq.get(f'https://fbref.com{url}')
        matches = pd.read_html(StringIO(html.text), match='Scores & Fixtures')[0]

        team = url.split('/')[-1].replace('-Stats', '').replace('-', ' ')
        season = year
        
        data = BeautifulSoup(html.text, 'html.parser')
        shooting_l = [l.get('href') for l in data.find_all('a') if l.get('href') and 'all_comps/shooting/' in l.get('href')][0]
        shooting_link = f'https://fbref.com{shooting_l}'
        time.sleep(7)
        shooting_html = rq.get(shooting_link)
        shooting = pd.read_html(StringIO(shooting_html.text), match='Shooting')[0].iloc[:-1]
        shooting.columns = shooting.columns.droplevel()
        matches = matches.drop(columns=['Referee', 'Match Report', 'Notes'], axis=1)

        try:
            season_data = matches.merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on='Date')
        except ValueError:
            continue

        season_data['team'] = team
        season_data['season'] = season
        print(season_data)
        seasons.append(season_data)
        time.sleep(7)
    

match_data = pd.concat(seasons)
match_data.columns = [c.lower() for c in match_data.columns]
match_data.to_csv('matches.csv')