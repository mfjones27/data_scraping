import os
import requests as rq
from bs4 import BeautifulSoup

os.makedirs('mls_logos', exist_ok=True)

url = 'https://www.mlssoccer.com/clubs/'

response = rq.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    img_tags = [l for l in soup.find_all('img')][1:30]

    for img_tag in img_tags:
        club_name = img_tag.get('alt').replace(' ', '_')
        src = img_tag.get('src')
        club_logo = rq.get(src).content

        with open(f'mls_logos/{club_name}.png', 'wb') as logo:
            logo.write(club_logo)

        print(f'Downloaded {club_name}\'s logo successfully.')
else:
    print('Attempt failed.')