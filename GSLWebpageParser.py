# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 11:09:16 2020

@author: akavcioglu
"""


import pandas as pd
import requests
from bs4 import BeautifulSoup


def GSLWebpageParser (URL):
    try:
        df = pd.read_html(URL, attrs={'class':'wikitable wikitable-bordered prizepooltable collapsed'})[0]
    except:
        try:
            URL += '/Code_S'
            df = pd.read_html(URL, attrs={'class':'wikitable wikitable-bordered prizepooltable collapsed'})[0]
        except:
            raise

    bad_columns = ['EPT Korea Pts', '₩ KRW', 'Points', 'WCS Points', 'WCS KR Pts']
    for col in bad_columns:
        if col in df.columns:
            df = df.drop(columns=[col])

    df = df.fillna('Teamless')
    df = df[df['$USD'] != '-']
    df = df[df['Player'] != 'TBD']
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('h1', class_='firstHeading')
    
    tournament_string = results.text.replace('\n','')
    df.insert(0, 'Tournament', tournament_string, True)
    df['$USD'] = df['$USD'].astype(str).apply(lambda x: str(x.replace('$','').replace(',',''))).astype(float)
    
    return df