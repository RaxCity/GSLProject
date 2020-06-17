# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 14:10:22 2020

@author: akavcioglu
"""


import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = 'https://liquipedia.net/starcraft2/2010_Sony_Ericsson_StarCraft_II_Open_Season_2'
def GSLWebpageParser(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    results = soup.find(id = 'mw-content-text')
    try:
        tables = results.find_all('table', class_ = 'wikitable wikitable-bordered prizepooltable collapsed')[0]
    except:
        URL += '/Code_S'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id = 'mw-content-text')
        tables = results.find_all('table', class_ = 'wikitable wikitable-bordered prizepooltable collapsed')[0]

    rows = tables.find_all('tr')
    indices = rows[0].find_all('th')
    
    col = []
    for index in indices:
        col.append(index.text.replace('\xa0',''))
    
    col.append('Race')
    col.append('Country')
    
    df = pd.DataFrame(columns = col)
    
    prevList = []
    for row in rows[1:]:
        player_list = []
        player_obj = row.find_all('td')
        
        try:
            int(player_obj[0]['rowspan'])
            for index in range(len(col)-2):
                player_list.append(player_obj[index].text)
        except:
            player_list = prevList
        player = row.find_all('a')
        try:
            country = player[0]['title']
            race = player[1]['title']
            name = player[2].text
        except:
            country = player[1]['title']
            race = player[2]['title']
            name = player[3].text
        
        player_list.append(race)
        player_list.append(country)
        
        s = pd.Series(player_list, index=col)
        s['Player'] = name
        s['Team'] = row.find_all('td', class_='prizepool-col-team')[0].text.replace('ZZZZZ','Teamless')
        
        place = s['Place']
        if place[1].isdigit():
            index_df = int(place[0:2])
        else:
            index_df = int(place[0])
        s.name = index_df
        df = df.append(s)
        prevList = player_list[:-2]

    bad_columns = ['EPT Korea Pts', '₩ KRW', '₩KRW', 'Points', 'WCS Points', 'WCS KR Pts']
    for col in bad_columns:
        if col in df.columns:
            df = df.drop(columns=[col])

    df = df.fillna('Teamless')
    df = df[df['$USD'] != '-']
    df = df[df['Player'] != 'TBD']
    
    
    results = soup.find('h1', class_='firstHeading')
    tournament_string = results.text.replace('\n','')
    df.insert(0, 'Tournament', tournament_string, True)
    df['$USD'] = df['$USD'].astype(str).apply(lambda x: str(x.replace('$','').replace(',',''))).astype(float)
    df['Country'].astype(str).apply(lambda x: str(x.replace('Korea (South)', 'South Korea').replace('United States of America', 'USA')))
    return df

df = GSLWebpageParser(URL)