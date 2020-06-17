# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 14:10:22 2020

@author: akavcioglu
"""


import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = 'https://liquipedia.net/starcraft2/2010_Sony_Ericsson_StarCraft_II_Open_Season_2'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id = 'mw-content-text')
tables = results.find_all('div', class_ = 'table-responsive')[0]

rows = tables.find_all('tr')
indices = rows[0].find_all('th')

col = []
for index in indices:
    col.append(index.text.replace('\xa0',''))

col.append('Race')
col.append('Country')

df = pd.DataFrame(columns = col)

place = ''
usd = ''
krw = ''

for row in rows[1:]:
    if row.find_all('td')[0].text[0] == '\xa0':
        player = row.find_all('a')
        try:
            country = player[0]['title']
            race = player[1]['title']
            name = player[2]['title']
        except:
            country = player[1]['title']
            race = player[2]['title']
            name = player[3]['title']        
        team = row.find_all('td')[1].text.replace('ZZZZZ','Teamless')
    else:
        place = row.find_all('td')[0].text.replace(' ', '')
        usd = row.find_all('td')[1].text
        krw = row.find_all('td')[2].text
        team = row.find_all('td')[4].text.replace('ZZZZZ','Teamless')
        
        player = row.find_all('a')
        try:
            country = player[0]['title']
            race = player[1]['title']
            name = player[2]['title']
        except:
            country = player[1]['title']
            race = player[2]['title']
            name = player[3]['title']
            
    if place[1].isdigit():
        index_df = place[0:2]
    else:
        index_df = place[0]

    s = pd.Series([place, usd, krw, name, team, race, country], index=col, name = index_df)
    df = df.append(s)